// Apple Vision for stream-trim's thumbnails. vision.py compiles this once
// and caches the binary.
//
//   vision faces <img>...                  one JSON line per image:
//                                          {"path", "faces": [{"box": [x, y, w, h], "quality"}]}
//   vision mask <img> <x> <y> <w> <h> <out.png>
//                                          writes an 8-bit mask, image-sized, of the one
//                                          person under the centre of that face box
//
// Boxes are in pixels, top-left origin.
import CoreGraphics
import CoreVideo
import Foundation
import ImageIO
import UniformTypeIdentifiers
import Vision

func fail(_ msg: String) -> Never {
    FileHandle.standardError.write(("ERROR: " + msg + "\n").data(using: .utf8)!)
    exit(1)
}

func load(_ path: String) -> CGImage {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fail("can't read \(path)") }
    return img
}

func faces(_ path: String) -> [String: Any] {
    let img = load(path)
    let w = Double(img.width), h = Double(img.height)
    let req = VNDetectFaceCaptureQualityRequest()
    do { try VNImageRequestHandler(cgImage: img, options: [:]).perform([req]) } catch { fail("\(error)") }
    let found: [[String: Any]] = (req.results ?? []).map { f in
        let b = f.boundingBox
        let box = [b.minX * w, (1 - b.maxY) * h, b.width * w, b.height * h].map { ($0 * 10).rounded() / 10 }
        return ["box": box, "quality": Double(f.faceCaptureQuality ?? 0)]
    }
    return ["path": path, "faces": found]
}

func mask(_ path: String, _ x: Double, _ y: Double, _ bw: Double, _ bh: Double, _ out: String) {
    let img = load(path)
    let handler = VNImageRequestHandler(cgImage: img, options: [:])
    let req = VNGeneratePersonInstanceMaskRequest()
    do { try handler.perform([req]) } catch { fail("\(error)") }
    guard let obs = req.results?.first else { fail("no person found") }
    // The label map is lower resolution than the image: find the label at the face centre.
    let labels = obs.instanceMask
    CVPixelBufferLockBaseAddress(labels, .readOnly)
    let lw = CVPixelBufferGetWidth(labels), lh = CVPixelBufferGetHeight(labels)
    let row = CVPixelBufferGetBytesPerRow(labels)
    let base = CVPixelBufferGetBaseAddress(labels)!.assumingMemoryBound(to: UInt8.self)
    let cx = min(lw - 1, max(0, Int((x + bw / 2) / Double(img.width) * Double(lw))))
    let cy = min(lh - 1, max(0, Int((y + bh / 2) / Double(img.height) * Double(lh))))
    let label = Int(base[cy * row + cx])
    CVPixelBufferUnlockBaseAddress(labels, .readOnly)
    if label == 0 { fail("no person under that face") }

    let scaled: CVPixelBuffer
    do { scaled = try obs.generateScaledMaskForImage(forInstances: IndexSet(integer: label), from: handler) }
    catch { fail("\(error)") }
    CVPixelBufferLockBaseAddress(scaled, .readOnly)
    defer { CVPixelBufferUnlockBaseAddress(scaled, .readOnly) }
    let mw = CVPixelBufferGetWidth(scaled), mh = CVPixelBufferGetHeight(scaled)
    let mrow = CVPixelBufferGetBytesPerRow(scaled)
    let mbase = CVPixelBufferGetBaseAddress(scaled)!
    var bytes = [UInt8](repeating: 0, count: mw * mh)
    for j in 0..<mh {
        let r = (mbase + j * mrow).assumingMemoryBound(to: Float32.self)
        for i in 0..<mw { bytes[j * mw + i] = UInt8(max(0, min(1, r[i])) * 255) }
    }
    guard let provider = CGDataProvider(data: Data(bytes) as CFData),
          let gray = CGImage(width: mw, height: mh, bitsPerComponent: 8, bitsPerPixel: 8, bytesPerRow: mw,
                             space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGBitmapInfo(rawValue: 0),
                             provider: provider, decode: nil, shouldInterpolate: false, intent: .defaultIntent),
          let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL,
                                                     UTType.png.identifier as CFString, 1, nil)
    else { fail("can't write \(out)") }
    CGImageDestinationAddImage(dest, gray, nil)
    if !CGImageDestinationFinalize(dest) { fail("can't write \(out)") }
}

let args = Array(CommandLine.arguments.dropFirst())
switch args.first {
case "faces":
    for p in args.dropFirst() {
        let data = try! JSONSerialization.data(withJSONObject: faces(p))
        print(String(data: data, encoding: .utf8)!)
    }
case "mask" where args.count == 7:
    let n = args[2...5].map { Double($0) ?? .nan }
    if n.contains(where: { $0.isNaN }) { fail("box must be numbers") }
    mask(args[1], n[0], n[1], n[2], n[3], args[6])
default:
    fail("usage: vision faces <img>... | vision mask <img> <x> <y> <w> <h> <out.png>")
}

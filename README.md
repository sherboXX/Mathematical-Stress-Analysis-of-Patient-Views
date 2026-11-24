# Mathematical Stress Analysis of Patient Views: Patient Room VR

**Live site:** https://sherboxx.github.io/Mathematical-Stress-Analysis-of-Patient-Views/

This is a phone VR experience (Google Cardboard-style: two screens plus lenses). It shows a hospital Med Surg patient
room from the bed, **sitting up** or **lying down (sleeping)**. Each candidate landscape is printed on the ceiling,
the curved fillet and the foot wall. The **original room** (tile ceiling) is included for comparison.

## Use it
1. Open the live site on your phone (it must be https, because phones only give motion sensors to https pages).
2. Choose the **ceiling picture** (Original room, B–F) and the **position** (sitting up / lying down).
3. Choose your **headset preset**, then fine-tune the **optics** (below). Use the calibration grid while tuning.
4. Tap **Enter VR (2 screens)**, put the phone in the headset and look ahead. The view recentres after a second.

### Headset optics
| Setting | What it does |
|---|---|
| Headset preset | Starting values: Cardboard v2 (IPD 63.9 mm, lens 39.3 mm, k1 0.34, k2 0.55), Cardboard v1, VR Box, none |
| Lens separation (IPD) | Distance between the two lens centres. The two images must fuse into one. |
| Screen-to-lens distance | Overall scale / zoom of the view. |
| k1, k2 | Barrel distortion that cancels the lens's pincushion distortion. Grid lines must look straight. |
| Vertical lens offset | Moves both lens centres up or down to match the headset's tray. |
| Field of view | Size of the visible circle for each eye. |
| Phone screen width | Converts millimetres to pixels. Measure the long side of the lit screen once. |

*Show split view behind settings* shows the two screens live under the sliders. Settings are saved on the phone.

### In the headset
- **Gaze menu:** look below the view (toward your feet when you are really lying down). Hold your gaze on a button
  for about 1 second to press it: pictures, *Sit up* / *Lie down*, *Recenter*, *Hide menu*, **comfort rating 1–5**.
- **Headset button (screen tap):** presses the button you are looking at; otherwise it shows the next picture.
  **Double tap:** shows Settings / Recenter / Exit.
- **Lying down:** *I am sitting* shows the ceiling straight ahead. *I am lying down myself* means you lie on your
  back and Recenter while looking up.
- **Ratings:** stored on the phone. Download them as CSV from the settings screen.

## How the room images were made
- The room is rendered in **Blender (Cycles)** from the patient's eyes as **stereo 360° panoramas**:
  equirectangular, omni-directional stereo with 64 mm eye distance, 3072×1536 per eye.
  - **Sitting up:** eye 0.78 m above the mattress. The image centre is the foot wall.
  - **Lying:** the image centre is the ceiling straight above, with the stereo axis along the body (head–foot),
    so the ceiling is sharp and in 3D.
- The ceiling pictures are AI-generated photographs: **RealVisXL V5.0** (an SDXL fine-tune, openrail++),
  img2img from a layout picture (river to the bottom of the wall, slopes down to the banks, flowers on both
  banks) with golden-hour prompts. They are printed on a continuous ceiling + 0.40 m fillet + foot wall surface
  that is UV-mapped by arc length.
- The project scores pictures with four visual-comfort metrics, judged from the bed: spectral slope alpha,
  fractal dimension D, discomfort index DI and brightness.
- **The app (`index.html`)** uses no libraries. One WebGL shader draws both eyes. For each pixel it converts the
  position behind the lens back to a viewing angle by inverting r' = r(1 + k1 r² + k2 r⁴). It also handles
  phone-gyroscope head tracking (DeviceOrientation), a gaze menu placed in the room with true stereo depth, and a
  calibration grid.

## Files
| File | Content |
|---|---|
| `index.html` | the whole app |
| `scenes/` | `<scene>_<sit|lie>_<L|R>.jpg` stereo panoramas + `manifest.json` |
| `serve.py` | optional: serve over HTTPS on your own Wi-Fi (self-signed certificate) instead of GitHub Pages |
| `prepare_scenes.py` | copies new Blender renders into `scenes/` (needs the full project folders) |

To test on a computer: `index.html?mode=preview&scene=B_golden_sunset&pose=lie` (single view, drag to look),
`?mode=stereo` (two screens), `&grid=1` (calibration grid).

## Blender renders of the ceiling pictures
[`renders/gallery.jpg`](renders/gallery.jpg) shows each picture in the room, starting with the original room, in
three views: lying (looking up), reclined 45° and a room overview. The single images are in `renders/`.

The four metrics measured on these Blender renders are in `renders/metrics_blender.json`. Targets: alpha 0.8–1.2,
D 1.30–1.50, DI ≤ 1.5, brightness 0.25–0.60.

| Picture | Lying: alpha / D / DI / brightness | Reclined 45°: alpha / D / DI / brightness |
|---|---|---|
| Original room | 1.525 miss / 1.373 / 0.361 / 0.750 miss | 1.478 miss / 1.312 / 0.319 / 0.687 miss |
| B · Golden sunset | 1.872 miss / 1.552 miss / 0.182 / 0.597 | 1.728 miss / 1.671 miss / 0.210 / 0.377 |
| C · Golden cascade | 1.848 miss / 1.529 miss / 0.188 / 0.590 | 1.701 miss / 1.681 miss / 0.216 / 0.374 |
| D · Poppies, alpenglow | 1.925 miss / 1.533 miss / 0.159 / 0.572 | 1.718 miss / 1.672 miss / 0.210 / 0.372 |
| E · Valley mist | 1.898 miss / 1.552 miss / 0.167 / 0.578 | 1.756 miss / 1.681 miss / 0.193 / 0.362 |
| F · Sun star | 1.883 miss / 1.444 / 0.170 / 0.563 | 1.643 miss / 1.620 miss / 0.249 / 0.374 |

The photo-real pictures bring brightness into range (the original white ceiling is too bright). As real
photographs, though, they miss alpha (too steep a spectrum) and D (too many detail features). A Fourier detail layer
can bring alpha into range, at some cost in realism.

## Credits and licences
- AI images: RealVisXL V5.0 (SG161222, openrail++), SDXL base 1.0 and the SDXL VAE fp16 fix (CreativeML Open
  RAIL++-M / MIT).
- Hospital room: third-party 3D model of a Med Surg patient room, rendered in Blender. The model's licence is
  still being confirmed for public use.

# Roadmap

Status: **Open**, **Spike** (feasibility unknown, test first). Nothing is tested on the watch yet.

## 0. Facts to settle first
- [ ] Exact model (Watch4/5/6/7/Ultra?) and One UI Watch version. Run `watch.py check`.
- [x] Wear OS confirmed (Galaxy Watch 4 or later), so the adb route applies. Still need the exact model from `watch.py check`.

## 1. Debloat
- [ ] `watch.py dump`, then split into batches: Samsung extras, Google extras, telemetry, health features you never use.
- [ ] Never-disable list: watch face service, SystemUI, Bluetooth, phone companion link (`com.samsung.android.app.watchmanager` side), Play services, input method, Samsung Health sensor service if you use any health feature.
- [ ] After each batch: reboot, check battery drain over 24h and that notifications still arrive. Log in `debloat/log.tsv`.
- [ ] Measure before/after: free RAM, idle battery per day, app open time.

## 2. Custom launcher (`home/`)
- [ ] **Spike:** can a third-party app become HOME on One UI Watch? Flattery says yes via binding a hardware button. Test with Flattery APK first.
- [ ] Round-screen layout: honeycomb or list drawer, rotary bezel / crown scrolling, big touch targets.
- [ ] Pinned apps only (5 to 8), everything else behind search or an "all apps" page.
- [ ] Always-on-friendly: black background (OLED), no animation when ambient.
- [ ] Glanceable complications: time, steps, battery, next calendar item.
- [ ] Tile for phone-less use: timer, flashlight, music control.

## 3. Efficiency
- [ ] No background services in the launcher; read data on resume only.
- [ ] Cache icons as pre-scaled bitmaps; no image libraries.
- [ ] Profile cold start with `adb shell am start -W`.

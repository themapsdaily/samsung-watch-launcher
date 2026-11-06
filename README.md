# watch

A custom home screen and a reversible debloat for a Samsung Galaxy Watch (Wear OS), with no root. Modelled on `../firetv-launcher`.

- **`debloat/`**: `watch.py` disables packages in batches with `pm disable-user --user 0`, never uninstalls, refuses a never-disable list, and can undo every step.
- **`home/`**: the custom launcher (`com.siddh.watchhome`), plain Kotlin or Java, no heavy libraries. Not started: see `ROADMAP.md`.
- **`design/`**: HTML mockups of the watch face and app grid, round 1.8 inch screen.

## Install (debloat only, works today)

Needs `adb` (`brew install android-platform-tools`). On the watch: Settings > About watch > Software > tap Software version 7 times, then Developer options > ADB debugging and Debug over Wi-Fi.

```bash
adb pair <ip>:<pair-port>        # code from the watch
adb connect <ip>:<port>
export ADB_SERIAL=<ip>:<port>
python3 debloat/watch.py check                       # model, Wear OS version, RAM, home app
python3 debloat/watch.py dump                        # save packages-<model>.txt for building batches
python3 debloat/watch.py disable debloat/batch1-samsung-extras.pkgs
python3 debloat/watch.py enable  all                 # undo everything
```

Package names differ per model and One UI Watch version. Always run `dump` first and check each batch against your own list before disabling.

## Reference repos (clone into `reference/`)

- [Flattery](https://github.com/lhforsythe/Flattery): Apple Watch style launcher, tested on Galaxy Watch 4. Best UI starting point.
- [Forigon](https://alternativeto.net/software/forigon/about): GPL-3.0 launcher with bubble drawer and virtual bezel scrolling.
- [Wear Gesture Launcher](https://github.com/henryzt/Wear-Gesture-Launcher): gesture-to-launch, old code.
- [AWatch](https://github.com/1hakr/AWatch) and [m8](https://github.com/rdnt/m8): other watch UI projects to skim.
- Debloat lists: gists by [ftpmorph](https://gist.github.com/ftpmorph/f9a060c206b0f027c4e621a41ad21d76), [dylanmtaylor](https://gist.github.com/dylanmtaylor/e839f4b83c2df313b0640032e730400d), [jbowdre](https://gist.github.com/jbowdre/ea3ae44ce6dcf31d17c73484e7479910). Treat as untested lists, verify against `dump`.
- Fire TV sibling: `../firetv-launcher` (Guard.java, Tidy, batch/undo pattern).

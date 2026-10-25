# Resume status

## Current status — 2026-10-25

- The native v2 package is in `work/xiaoba/native/`: `pet.json` and `spritesheet.webp`. It contains nine animation rows and sixteen look directions.
- `work/安装小巴.ps1` installs and selects Xiaoba in the local Codex desktop app. It was run on the current machine on 2026-10-23; the updated sprite was reinstalled on 2026-10-25.
- On 2026-10-25, green chroma spill was removed from the complete atlas, and a neighboring-frame fragment was removed from review row frame 1. The action overview was regenerated from the updated sprite.
- The user requested direct installation and PR submission without final full-atlas quality validation. That validation remains undone.
- The notes below record the earlier 2026-10-22 production state and should not be read as the current package status.

## Earlier production notes

- User authorized system Python C:/Users/cwrt/miniconda3/python.exe because bundled workspace runtime is unconfigured. Pillow 12.2.0 verified. Use this full executable path for scripts.
- Canonical base preserved and approved.
- Idle source repair v3 selected, independent component extraction and inspect_frames passed. Frames at qa/rows/idle/frames/idle.
- Original waving source recovered from generated_images, component extraction and inspect_frames passed, but user says wave is stiff. Parent 4-frame review found waving hand switches screen side between frames 1 and 2/3; body/face too rigid. Waving must be visually repaired despite structural QA pass.
- Current immediate user priority: fewer initial states; focus on making waving good first. Other generation stopped/backlogged after in-flight results. No installation or Pets record mutation yet.
- wave_polish worker assigned coherent 4-frame looping raised SAME screen-left hand, screen-right hand holding core, wrist swing, shoulder/elbow, head/face/hair follow-through; no snap from repeated raising/lowering. Keep native four-frame compatibility.
- Jumping and waiting outputs copied to decoded only; not deterministically or visually approved, and not marked complete.
- Running-right has repeated transient transport failures and remains pending. Other requested standard states and look rows have not been generated.
- outputs/安装小巴.ps1 is a staged installer only. It cannot install until validated native package exists. It expects sha256 in validation-extended.json; use newer Pets validator (it records hash) in addition to hatch validator before packaging. Native package path .codex/pets/xiaoba with pet.json and spritesheet.webp. Existing desktop config has selected-avatar-id=codex and avatar-overlay-pet-visible=true.
- No writes outside workspace authorized yet; request exact package/config filesystem permissions only once final package is concrete and validated.
- Original generated files retained because imagegen tool says leave originals in place unless user requests deletion. Do not delete originals under .codex/generated_images.
- Updated manifest references compact exact downscales, original art preserved. Compact canonical ~328KB and source ~123KB. All later jobs attach listed guide plus both refs.

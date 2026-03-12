# video-ffmpeg-assemble.SKILL.md

**용도**: ffmpeg 씬 조립 및 편집  
**사용 에이전트**: video-agent  
**버전**: 1.0

---

## 📥 입력

- reels/scenes/{scene_id}.mp4 (3~4개 씬)
- bgm.mp3 (선택)

---

## 📤 출력

- reels/final_reel.mp4 (20초 이내)

---

## 🔧 ffmpeg 명령어

### 씬 조립
```bash
ffmpeg -i scene1.mp4 -i scene2.mp4 -i scene3.mp4 \
  -filter_complex '[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]' \
  -map '[v]' \
  -c:v libx264 -preset slow -crf 18 \
  combined.mp4
```

### BGM 삽입 (페이드 인/아웃)
```bash
ffmpeg -i combined.mp4 -i bgm.mp3 \
  -filter_complex '[1:a]afade=t=in:st=0:d=1,afade=t=out:st=17:d=3[a]' \
  -map '0:v' -map '[a]' \
  -shortest \
  -c:v copy \
  final_reel.mp4
```

### 자막 오버레이 (developer 담당)
```bash
ffmpeg -i final_reel.mp4 \
  -vf "drawtext=text='저장 필수 ✨':fontfile=/path/to/font.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-100" \
  final_with_caption.mp4
```

---

## 📋 릴스 구성 예시

**20초 릴스**:
- Scene 1 (훅): 3초
- Scene 2 (바디): 8초
- Scene 3 (아이템): 5초
- Scene 4 (CTA): 4초

---

## ✅ 검증

### [ ] 총 길이: 20초 이내
### [ ] BGM 볼륨: 영상 대비 -10dB
### [ ] 해상도: 1080×1920 (9:16)
### [ ] 코덱: H.264

---

**최종 업데이트**: 2026-03-06 04:01

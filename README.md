# Schumann Resonance Data Monitor

SchumannResonanceLive.com APIから15分間隔でシューマン共振データを蓄積し、GitHub Pagesで可視化するプロジェクト。

## 取得データ

- **周波数**: SR1〜SR5（第1〜第5モード）
- **振幅**: 各モードのamplitude値
- **ピーク**: 各モードのpeak周波数
- **パワー**: 各モードのpower値
- **品質**: signal_strength, SNR, noise_level, quality_score, stability
- **トレンド**: 各モードの上昇/下降

## セットアップ手順

### 1. GitHubリポジトリを作成

1. GitHub.comで新しいリポジトリを作成
   - リポジトリ名: `schumann-monitor`（任意）
   - Public にする（GitHub Pages無料利用のため）
2. このフォルダの中身を全てpush

### 2. GitHub Pagesを有効化

1. リポジトリの Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main` / `/ (root)`
4. Save

### 3. GitHub Actionsを有効化

1. リポジトリの Settings → Actions → General
2. "Allow all actions" を選択
3. Workflow permissions: "Read and write permissions" を選択
4. Save

### 4. 初回データ取得（手動）

1. リポジトリの Actions タブ
2. "Schumann Resonance Data Collector" を選択
3. "Run workflow" をクリック
4. 成功すると `data/schumann_log.csv` が作成される

以降は15分ごとに自動実行されます。

## ファイル構成

```
schumann-monitor/
├── .github/workflows/
│   └── collect.yml      # GitHub Actions ワークフロー
├── data/
│   └── schumann_log.csv # 蓄積データ（自動生成）
├── collect.py           # データ取得スクリプト
├── index.html           # 可視化ダッシュボード
└── README.md
```

## コスト

- **API**: 無料（認証不要、CC BY 4.0）
- **GitHub Actions**: 15分間隔 → 月約960分（無料枠2,000分以内）
- **GitHub Pages**: 無料

## データソース

- API: https://schumannresonancelive.com/schumann_api.php
- 元データ: Space Observing System, Tomsk State University, Russia
- ライセンス: CC BY 4.0

## 検証方法

蓄積したデータのグラフを以下と目視比較:
- トムスク srf.jpg: http://sos70.ru/srf.jpg
- HeartMath Spectrogram Calendar: https://www.heartmath.org/gci/gcms/live-data/spectrogram-calendar/

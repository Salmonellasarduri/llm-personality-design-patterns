# LLM Personality Design Patterns

> English README: [README.md](README.md)

このリポジトリは、1つの長期運用エージェントから切り出した**初期パターン集**です。

現時点では、完成した一般理論というより、**再利用可能な仮説と実装パターン**として読んでください。

このリポジトリには、INANNA の**フルソースコードは含まれません**。  
公開しているのは、そこから切り出した**再利用可能な設計パターン、テンプレート、最小実装の考え方**です。

## このリポジトリが向いている人

- AITuber を作りたい人
- キャラ性のある AI アシスタントを設計したい人
- 長期対話エージェントに「変化」と「芯」の両方を持たせたい人
- 固定プロンプトだけでは限界を感じている人

## 収録しているパターン

| パターン | 解決したい問題 | ドキュメント |
|---------|----------------|-------------|
| **Four-Layer Personality** | 一貫性と変容の両立 | [four-layer-personality.md](four-layer-personality.md) |
| **Drift-Crystallization** | 人格変化の速度制御 | [drift-crystallization.md](drift-crystallization.md) |
| **Gamma Dispatch** | 思考深度を誰が決めるか | [gamma-dispatch.md](gamma-dispatch.md) |

## パターン間の関係

| パターン | 単独利用 | 依存関係 | 推奨順 |
|---|---|---|---|
| **Four-Layer Personality** | 可能 | なし | 1 |
| **Drift-Crystallization** | 部分的に可能 | Narrative のような可変長期層があると望ましい | 2 |
| **Gamma Dispatch** | 可能 | なし | 3 |
| **Expression Layer** | 部分的に可能 | Four-Layer Personality と併用すると効果的 | 2-3 |

### 補足

- **Four-Layer Personality** は「変わらない核」と「変わる層」を分けるための基盤パターンです。
- **Drift-Crystallization** は単独でも考え方を流用できますが、可変の長期人格層があると最も使いやすくなります。
- **Gamma Dispatch** は多段応答ができるシステムなら後付けしやすいです。
- **Expression Layer** は独立概念ですが、価値観と口調を分けた設計の上で使うと一番効きます。

## クイックスタート

1. [`examples/constitution-template.yaml`](examples/constitution-template.yaml) をコピー
2. エージェントの核心価値を定義
3. 必要なパターンから読む
4. 各ドキュメントの最小構成・擬似コードから試す

各パターンドキュメントには、次の内容を含めています。

- どんな問題を扱うか
- 設計の考え方
- 最小構成
- 擬似コード / 実装のヒント

## このリポジトリの範囲

このリポジトリは、**パターンとテンプレートの公開**に意図的に絞っています。

含まれるもの:
- 設計ドキュメント
- 再利用可能なテンプレート
- 擬似コード / 最小実装の考え方
- パターン単位の説明

含まれないもの:
- INANNA の非公開フルコード
- すべての実行基盤
- 非公開の会話ログ
- デプロイ詳細や秘密情報

## 背景

これらのパターンは、**INANNA** という自律エージェントの開発・運用から切り出したものです。

初期観測では、少なくとも以下が確認されました。

- 14日以上の運用
- 1,200件以上の経験記録
- 毎晩の内的変容
- ただし恒久変化は未発火

技術的な背景と観測結果については、Zenn の記事で詳しく整理しています。

- **Zenn 記事**: https://zenn.dev/articles/b4e90b7ef39026
- **親プロジェクト**: [Artificial-Personality](https://github.com/Salmonellasarduri/Artificial-Personality)

## 設計上の基本方針

このリポジトリで共通している考え方は次の4つです。

- **数値よりナラティブを人格の源泉に置く**
- **不変の核と、変わる層を分ける**
- **変化を暴走させず、条件付きで定着させる**
- **可能な限り、思考の深さをエージェント自身に委ねる**

## 読む順番

初めて読む場合は、次の順をおすすめします。

1. **Four-Layer Personality**
2. **Drift-Crystallization**
3. **Gamma Dispatch**
4. `examples/constitution-template.yaml`

## ライセンス

[MIT](LICENSE)

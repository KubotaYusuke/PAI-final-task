# PAI最終課題：受動漂流型・蚊型救助ドローンのスウォーム探索

東京大学 松尾・岩澤研究室「Physical AI応用編」最終課題提出用リポジトリです。

## 概要
災害現場での生存者探索を想定し、風の力を利用して省電力で拡散する「受動漂流（パッシブ・ダイナミクス）」と、要救助者シグナルを検知した際のみアクティブ集積する「超軽量エッジAI」を組み合わせたスウォーム探索シミュレーションです。

## 構成ファイル
- `mosquito_swarm.py`: ROS 2 Humble / RViz2 用の移動・変色制御ノード

## 動作環境
- Ubuntu 22.04 LTS (ROS 2 Humble / Docker)
- Python 3
- RViz2 (Topic: `/mosquito_swarm_markers`)

## デモ動画
- YouTube: https://youtu.be/D3kw-4UBT1w

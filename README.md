"# B4program" 

・data_processor.py
入力:人が写った(街路空間の)画像
出力:トリミングされた人の顔とそれに対応する人の特徴(年齢、性別、感情など)がcsv形式で出力されます。
  
FaceAPIを使っているので、キーは各自で取得してください。

例外処理に甘い点やファイル名の拡張子以外に"jpg"とか入っていると正しく動かなかったり冗長な部分もあったりするので、後日リファクタリングを行う予定です。

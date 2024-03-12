# VoiceNotifier

discordのボイスチャンネルを監視して入退室があった場合にテキストチャンネルにテキスト投げて通知を鳴らすやつです。  
今のところ以下の機能があります。

- 監視するボイスチャンネルの指定
- テキストを投げるテキストチャンネルの指定
- 投げるテキストの内容の指定

## 使い方
操作はスラッシュコマンドで  
設定さえすりゃあとは勝手に入退室監視するんで  
##### /voicenotifier_man
各コマンドのマニュアル出すやつです。  
~~まあここに書いてあるのと同じことしか言わないんだけど~~  
使用方法: /set_text_channel [command]
##### /set_text_channel
通知を送信するテキストチャンネルを設定します。既に指定されている場合は置き換えられます。つまり指定できるテキストチャンネルは一つだけです。  
使用方法: /set_text_channel [テキストチャンネル]
##### /add_voice_channel
ボイスチャンネルを監視リストに追加します。複数のボイスチャンネルを監視したい場合は一つずつ追加してください。
使用方法: /add_voice_channel [ボイスチャンネル]  
##### /remove_voice_channel
監視リストからボイスチャンネルを削除します。複数のボイスチャンネルを監視から外したい場合は一つずつ追加してください。  
使用方法: /remove_voice_channel [ボイスチャンネル]  
##### /set_join_message
入室時に送信するメッセージの形式を指定します。{member}、{channel}と書くと送信時に実際のユーザ名やチャンネル名で動的に置き換えられます。  
使用方法: /set_join_message [message]  
 例: /set_join_message [{channel}]:green_circle:{member}  
##### /set_leave_message
退室時に送信するメッセージの形式を指定します。{member}、{channel}と書くと送信時に実際のユーザ名やチャンネル名で動的に置き換えられます。  
使用方法: /set_join_message [message]  
 例: /set_join_message [{channel}]:red_circle:{member}  
  
  
  
  
  
  
## サーバ動かしたい人
dockerfileもcomposeもとりあえず置いてあるんで雑に動かすだけならそれ使えばすぐに動かせるはず。  
botのためのトークンは何とかして用意してください。環境変数で渡すのでcompose使うならenvironment:のTOKENのところに、Dockerfileだけ使ってcomposeしないならENV追記するなりしてやってください。  
身内用に作ったやつが元なんで招待リンクなんて用意してませんし、用意する予定も現状無いです。  
クオリティにも期待しないでくだせ。そんな真面目に検証なぞしとらんので。  
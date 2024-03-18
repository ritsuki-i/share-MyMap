// Google Maps APIを読み込むための関数
function loadGoogleMapsAPI() {
  // script要素を作成
  let script = document.createElement('script');
  // APIのURLを設定。APIキーとバージョン情報を含む
  script.src = `https://maps.googleapis.com/maps/api/js?key=${mapParams.googleMapKey}&v=weekly`;
  // script要素をdocumentのheadに追加
  document.head.appendChild(script);
  // スクリプトが読み込まれたら、マップを初期化する関数を実行
  script.onload = () => {
    initMap(mapParams.lat, mapParams.lng, mapParams.zoom);
  };
}

// Googleマップを初期化し、マーカーとインフォウィンドウを設定する関数
function initMap(lat, lng, zoom) {
  // Googleマップのインスタンスを作成。指定された緯度、経度、ズームレベルで中心を設定
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: zoom,
    center: {lat: mapParams.lat, lng: mapParams.lng},
  });

  // マップマーカーの情報があれば、マーカーをマップに追加
  if (mapParams.mapMarker && mapParams.mapMarker.lat && mapParams.mapMarker.lng) {
    let marker = new google.maps.Marker({
      position: {lat: parseFloat(mapParams.mapMarker.lat), lng: parseFloat(mapParams.mapMarker.lng)},
      map,
      title: mapParams.mapMarker.title ? mapParams.mapMarker.title : 'No Title',
    });

    // マーカーがクリックされたら、インフォウィンドウを表示
    marker.addListener('click', () => {
      infoWindow.setContent(mapParams.mapMarker.description ? mapParams.mapMarker.description : 'No Description');
      infoWindow.open(map, marker);
    });
  }

  // インフォウィンドウのインスタンスを作成
  let infoWindow = new google.maps.InfoWindow();

  // マップがクリックされた場合の処理。インフォウィンドウを新しい位置に表示し、フォームを含める
  map.addListener("click", (mapsMouseEvent) => {
    // 既存のインフォウィンドウがあれば閉じる
    if (infoWindow) infoWindow.close();

    // クリックされた位置の緯度経度を取得
    const latLng = mapsMouseEvent.latLng.toJSON();
    infoWindow = new google.maps.InfoWindow({
      position: latLng,
    });

    // インフォウィンドウに表示する内容を設定。場所の名前と説明を入力するフォーム
    infoWindow.setContent(
      `<form action="/my-map" method="post">
        <input type="hidden" name="form_type" value="submit_location">
        <input type="hidden" id="lat" name="lat" value="${latLng.lat}">
        <input type="hidden" id="lng" name="lng" value="${latLng.lng}">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name"><br>
        <label for="description">Description:</label>
        <input type="text" id="description" name="description"><br>
        <input type="submit" value="Submit">
      </form>`
    );

    // インフォウィンドウを開く
    infoWindow.open(map);
  });
}

// Google Maps APIの読み込みを開始する
loadGoogleMapsAPI();

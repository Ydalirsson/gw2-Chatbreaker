module.exports = {
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      builderOptions: {
        "productName": "Chatbreaker",
        "appId": "org.yourProductName",
        "win":{
          "icon": "public/icon.png",
          "target": ["nsis", "msi"]
        },
        "directories":{
          "output": "release"
        }
      }
    }
  }
};

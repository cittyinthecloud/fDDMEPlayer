import { app, BrowserWindow, screen, ipcMain, shell, App } from 'electron';
import * as path from 'path';
import * as url from 'url';
import { launchMod, installMod } from './launcher/launcher';
import { path as appRoot } from "app-root-path"
import * as moddb from './launcher/moddb'
import { installDDLC } from './launcher/install';
import * as Store from "electron-store";

let win, serve;
const args = process.argv.slice(1);
serve = args.some(val => val === '--serve');

function createWindow() {

  const electronScreen = screen;
  const size = electronScreen.getPrimaryDisplay().workAreaSize;

  // Create the browser window.
  win = new BrowserWindow({
    x: 0,
    y: 0,
    width: size.width,
    height: size.height
  });

  if (serve) {
    require('electron-reload')(__dirname, {
     electron: require(`${__dirname}/node_modules/electron`)});
    win.loadURL('http://localhost:4200');
  } else {
    win.loadURL(url.format({
      pathname: path.join(__dirname, 'dist/index.html'),
      protocol: 'file:',
      slashes: true
    }));
  }

  win.webContents.openDevTools();

  // Emitted when the window is closed.
  win.on('closed', () => {
    // Dereference the window object, usually you would store window
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    win = null;
  });
}

let persistent: Store;

function getPersistent(app: App): Store {
  return persistent || (persistent = new Store({
    defaults: {
      "vanillaInstalled": false
    },
    cwd: app.getPath("userData")
  }))
}

try {

  // This method will be called when Electron has finished
  // initialization and is ready to create browser windows.
  // Some APIs can only be used after this event occurs.
  app.on('ready', createWindow);

  // Quit when all windows are closed.
  app.on('window-all-closed', () => {
    // On OS X it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
      app.quit();
    }
  });

  app.on('activate', () => {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (win === null) {
      createWindow();
    }
  });

  ipcMain.on("launch", (event, mod) => {
    (async () => {
        try {
          await launchMod(mod)
          event.sender.send("launchReply",{success : true, mod: mod})
        } catch (e) {
          event.sender.send("launchReply",{success : false, error: e.toString(), mod: mod})
        }
      })();
  });

  ipcMain.on("getMods", (event) => {
    (async () => {
      event.sender.send("modlist", await moddb.getMods())
    })();
  })

  ipcMain.on("openExternal",(event, url) => {
      shell.openExternal(url)
  })

  ipcMain.on("installDDLC",(event, path) => {
    installDDLC(path).then(()=>{
      event.sender.send("DDLCInstalled")
      getPersistent(app).set({
        "vanillaInstalled": true,
      })
    })
  })

  ipcMain.on("installMod",(event, args) => installMod(args.mod, args.path).then(() => event.sender.send("ModInstalled")))
} catch (e) {
  // throw e;
}

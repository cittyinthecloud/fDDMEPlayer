# fDDMEPlayer

**[Download from releases here](https://github.com/famous1622/fDDMEPlayer/releases)**

Downloading straight this repository will cause you to end up with a in-development version of the launcher, where bugs will be more likely to occur.

A mod launcher for DDLC.



## Developer instructions:

Clone this repository locally :

``` bash
git clone https://github.com/maximegris/angular-electron.git
```

Install dependencies with npm :

``` bash
npm install
```

## Build for development
```bash
npm start  
```

## Building
|`npm run build`| Build the app. Your built files are in the /dist folder. |
|`npm run build:prod`| Build the app with Angular aot. Your built files are in the /dist folder. |
|`npm run electron:local`| Builds your application and start electron
|`npm run electron:linux`| Builds your application and creates an app consumable on linux system |
|`npm run electron:windows`| On a Windows OS, builds your application and creates an app consumable in windows 32/64 bit systems |
|`npm run electron:mac`|  On a MAC OS, builds your application and generates a `.app` file of your application that can be run on Mac |

# Python + asyncio + rx + gstreamer + curses music player

All the data is kept in SQLite.

## Basic concepts
* **track** - a metadata for a music piece
* **track stream** - a stream of music data for a **track**
* **library** - keeps all your **tracks**
* **playlist** - a named subset of your **library**
* **provider** - an entity that delivers **track stream** e.g. Youtube, Spotify, local drive
* **cloud** - a service which we **sync** to e.g. Google Drive, AWS S3
* **sync** - a process of syncing your **library** with a **cloud**
* **command** - a piece of code invokable by keybinding or **command palette**

## Ripping
* **rip** - downloads the **track stream** from **provider** to your local drive. Automatically adds the **track** to the **library** if it's not there yet.
* **rip library** - tries to rip every **track** in the **library**
* **rip current playlist** - tries to rip every **track** in the current **playlist**

## Cloud sync
The **sync** is not automatic. It always have to be triggered manually. There are several commands here.
* **sync: push library** - pushes the SQLite database to a **cloud**
* **sync: pull library** - pulls the SQLite database from a **cloud**
* **sync: push track** - pushes the selected **track** to a **cloud** if **ripped**
* **sync: pull track** - pulls the selected **track** from a **cloud** if available
* **sync: push all tracks** - like above but for all tracks
* **sync: pull all tracks** - like above but for all tracks

## Feed
TODO

## UI components:
* LayoutComponent
* ListComponent
* TableComponent
* ProgressBarComponent
* InputComponent
* ErrorBoxComponent

## UI views
* **TracksView** - TableComponent
* **PlaylistView** - ListComponent
* **CommandPaletteView** - ListComponent, InputComponent
* **SearchView** - InputComponent

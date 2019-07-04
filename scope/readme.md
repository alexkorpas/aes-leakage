#### Installation (Windows)
1. Use `.\easy_scope\extract_all` to extract the executables.
1. Use `.\easy_scope\EasyScopeX_setup.exe` to install EasyScope.

#### Usage (Windows)

##### Setting up
1. Use `.\easy_scope\MiniMouseMacro.exe` to start the mouse macro runner.
1. Use the button in the bottom right corner to load the instructions from `.\easy_scope\scope_[Display_resolution].mmmacro` into MiniMouseMacro, for your respective display resolution.
1. Start EasyScope.
1. Select your scope from the ribbon: scope > add device

##### Running the trace acquisition loop  
1. Run the main function in `.\app.py` to prime the trace acquisition loop.
1. In EasyScope, save a dummy trace from the ribbon: waveform > save.
1. Press save in the dialog. Save a dummy file in the trace storage directory, 
`.\data\traces`.
1. The creation of the dummy file will start the trace acquisition loop. This loop can be interrupted at any time by spamming `<cmd> + F6`.
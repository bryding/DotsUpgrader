# Unity DOTS Upgrader

This tool converts components marked with [GenerateAuthoringComponent] to the new Entities 1.0 format.

See the [Official Upgrade Guide](https://docs.unity3d.com/Packages/com.unity.entities@1.0/manual/upgrade-guide.html) for detailed information on upgrading your project from .51 to 1.0. This tool automates the `Remove GenerateAuthoringComponent` section of the official upgrade guide.

### Example Usage

`python dotsupgrader.py --dir C:/YourGame/Assets/Scripts/EcsComponents --stage 1 --commit true`

### Steps to upgrade (note: do NOT upgrade to entities 1.0 until this guide tells you to!)

1. In stage 1, every IComponentData and IBufferElementData in the directory you specify (recursively) will be evaluated for the potential ugprade. If a given file contains the `[GenerateAuthoringComponent]` attribute, the script will attempt to add a monobehaviour corresponding to the old authoring component that Unity used to generate for you; it will also rename the file accordingly.
    - note that this tool assumes you are using `[GenerateAuthoringComponent]` attributes alone, meaning, you can't have multiple attributes like `[GenerateAuthoringComponent, Serializable]`. Maybe I'll fix this at some point when I'm not feeling lazy.
1. Verify your .51 project still works as expected
1. Upgrade to Entities 1.0 and the recommended Unity version.
1. Run stage 2. This will generate the Baker

### Script options

  -h, --help            show this help message and exit

  --dir DIR             The top level directory containing all of the .cs files that need to be updated. (default: ./sandbox/forModify)

  --stage {1,2}         Select stage 1 to update the file to add the monobehaviour authoring component. After stage 1 is complete, update to Entities 1.0, and then run   
                        stage 2 to create the Baker (default: 1)

  --commit {true,false}
                        Set to false to merely print out potential results, no files will be changed. True will update the files (default: false)

### Requirements

This script was tested using Python 3.10, other 3.x version should work in theory...
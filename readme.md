# Project Title

Ngrok for Magento2 local test

## Getting Started

This script can help you easily to test for request which require "https",

it will replace the base url of your magento2 project, and restore the base url when exit this script.

### Usage

* add one server name for your nginx config of your magento2 project.

```bash
server {
     server_name *.ngrok.io; #add this line in server term
}
```
* go to your magento2 project root directory first, then run the script.


```bash
# cd /to/your/magento2/project/
#/path/to/ngrok-for-magento2.py -l=LOCALDOMAIN -r=RESTOREDOMAIN
```


## Deployment

Add additional notes about how to deploy this on a live system


## Authors

* **Glenn Checg** - *NgrokForMagento2* - [Glenn Checg](https://github.com/GlennCheng)

See also the list of [NgrokForMagento2](https://github.com/GlennCheng/NgrokForMagento2) who participated in this project.

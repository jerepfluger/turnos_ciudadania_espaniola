import platform


def retrieve_firefox_binary_path_based_on_os(current_binary_path):
    current_os = platform.system()
    if current_os == 'Linux':
        return current_binary_path
    elif current_os == 'Windows':
        return 'C:\\Program Files\\Mozilla Firefox15\\Firefox.exe'
    else:
        return '/Applications/Firefox.app/Contents/MacOS/firefox'


def retrieve_chrome_binary_path_based_on_os(current_binary_path, browser_name):
    current_os = platform.system()
    if current_os == 'Linux':
        return current_binary_path
    elif current_os == 'Windows':
        return 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    else:
        if browser_name == 'chrome':
            return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        return '/Applications/Chromium.app/Contents/MacOS/Chromium'

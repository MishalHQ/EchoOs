# EchoOS Smart Application Management Guide

## 🚀 **Intelligent App Management System**

EchoOS now features **smart application management** that intelligently handles running applications. No more duplicate windows or confusion - EchoOS knows when apps are already running and acts accordingly!

## 🎯 **Smart Behavior Examples**

### **🌐 Browser Applications**
- **Chrome is running** + Say "open chrome" → **Opens new tab** (not new window)
- **Firefox is running** + Say "go to firefox" → **Opens new tab**
- **Edge is running** + Say "launch edge" → **Opens new tab**

### **📱 Other Applications**
- **Word is running** + Say "open word" → **Brings Word to front**
- **Excel is running** + Say "go to excel" → **Brings Excel to front**
- **Notepad is running** + Say "launch notepad" → **Brings Notepad to front**

### **🆕 New Applications**
- **App not running** + Say "open [app]" → **Launches new instance**

## 🎤 **Enhanced Voice Commands**

### **🔄 App Switching Commands**
- **"go to chrome"** - Switch to Chrome (opens new tab if running)
- **"switch to word"** - Switch to Microsoft Word
- **"bring to front excel"** - Bring Excel to the front
- **"open chrome"** - Open Chrome (new tab if running)

### **🆕 New Tab/Window Commands**
- **"new tab"** - Open new tab in current browser
- **"new window"** - Open new window in current app

### **❌ Close Commands (Unchanged)**
- **"close chrome"** - Close Chrome completely
- **"close all tabs"** - Close all applications
- **"close word"** - Close Microsoft Word

## 🧠 **How It Works**

### **1. Process Detection**
EchoOS checks if an application is already running by:
- **Process Name Matching**: Checks running processes
- **Executable Path Matching**: Matches by executable name
- **App Name Matching**: Matches by application name

### **2. Smart Decision Making**
- **Browsers**: Opens new tab (Ctrl+T)
- **Other Apps**: Brings to front or activates window
- **Not Running**: Launches new instance

### **3. Fallback Handling**
- **No pyautogui**: Falls back to launching new instance
- **Window Not Found**: Uses Alt+Tab to cycle windows
- **Error Handling**: Graceful error messages

## 🎯 **Voice Command Examples**

### **Browser Management**
```
"open chrome" → Opens Chrome (new tab if running)
"go to firefox" → Switches to Firefox (new tab if running)
"new tab" → Opens new tab in current browser
"close chrome tabs" → Closes only Chrome
```

### **Application Management**
```
"open word" → Opens Word (brings to front if running)
"switch to excel" → Switches to Excel
"bring to front notepad" → Brings Notepad to front
"close word" → Closes Word completely
```

### **System Management**
```
"close all tabs" → Closes all applications
"new window" → Opens new window in current app
"minimize" → Minimizes current window
"maximize" → Maximizes current window
```

## 🔧 **Technical Details**

### **Process Detection Methods**
1. **psutil Library**: Primary method for process detection
2. **Windows tasklist**: Fallback for Windows systems
3. **Process Name Matching**: Matches executable names
4. **App Name Matching**: Matches application names

### **Smart Handling Logic**
```python
if app_is_running:
    if is_browser:
        open_new_tab()
    else:
        bring_to_front()
else:
    launch_new_instance()
```

### **Supported Browsers**
- **Google Chrome**: Opens new tab
- **Mozilla Firefox**: Opens new tab
- **Microsoft Edge**: Opens new tab
- **Safari**: Opens new tab
- **Opera**: Opens new tab

## 🎨 **User Experience Benefits**

### **✅ No More Duplicate Windows**
- **Smart Detection**: Knows when apps are running
- **Appropriate Action**: New tab vs new window vs bring to front
- **Clean Desktop**: No cluttered duplicate windows

### **✅ Intuitive Behavior**
- **Natural Commands**: "go to chrome" works as expected
- **Context Aware**: Different behavior for different app types
- **Consistent Experience**: Predictable behavior across apps

### **✅ Efficiency**
- **Faster Access**: No waiting for new app launches
- **Better Workflow**: Seamless app switching
- **Reduced Confusion**: Clear, predictable behavior

## 🛠️ **Installation Requirements**

### **Required Libraries**
- **psutil**: For process detection
- **pyautogui**: For keyboard shortcuts and window management

### **Installation**
```bash
pip install psutil pyautogui
```

### **Optional Features**
- **pyautogui**: Enables new tab/window and window switching
- **Without pyautogui**: Falls back to launching new instances

## 🎯 **Best Practices**

### **Voice Command Tips**
1. **Be Specific**: "go to chrome" vs "open chrome"
2. **Use Natural Language**: "switch to word" works well
3. **Browser Commands**: Use "new tab" for browsers
4. **App Commands**: Use "open" for other applications

### **Workflow Optimization**
1. **Keep Apps Open**: Let EchoOS manage running apps
2. **Use Switching**: "go to" commands for efficiency
3. **Browser Workflow**: Use "new tab" for web browsing
4. **App Workflow**: Use "open" for document editing

## 🚨 **Troubleshooting**

### **Common Issues**

1. **"App not switching"**
   - Check if pyautogui is installed
   - Verify app name spelling
   - Try "bring to front [app name]"

2. **"New tab not opening"**
   - Ensure you're in a browser
   - Check pyautogui installation
   - Try "go to [browser name]" first

3. **"App not detected as running"**
   - Check process name in Task Manager
   - Try different app name variations
   - Use "open [app name]" to launch new instance

### **Debug Information**
- **Check Console**: Look for process detection messages
- **Verify Installation**: Ensure psutil and pyautogui are installed
- **Test Commands**: Try different voice command variations

## 🎉 **Benefits Summary**

### **🚀 Efficiency**
- **No Duplicate Windows**: Smart detection prevents clutter
- **Faster Access**: New tabs instead of new windows
- **Better Workflow**: Seamless app management

### **🎯 Intelligence**
- **Context Aware**: Different behavior for different apps
- **Process Detection**: Knows what's running
- **Smart Decisions**: Appropriate actions for each situation

### **🎨 User Experience**
- **Intuitive Commands**: Natural language processing
- **Predictable Behavior**: Consistent across all apps
- **Error Handling**: Graceful fallbacks and error messages

---

**EchoOS v2.0** - Smart Application Management
*Intelligent app handling that knows what's running and acts accordingly*

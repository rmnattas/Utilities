/*
* Copyright (c) 2015 Razeware LLC
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*/

import Cocoa
import WebKit

class QuotesViewController: NSViewController {
    @IBOutlet var webKitView: WebView!
  let quotes = Quote.all

  var currentQuoteIndex: Int = 0 {
    didSet {
      //updateQuote()
        loadPage()
    }
  }

    func loadPage(){
        let pasteboard = NSPasteboard.general()
        var clipboardItems: [String] = []
        for element in pasteboard.pasteboardItems! {
            if let str = element.string(forType: "public.utf8-plain-text") {
                clipboardItems.append(str)
            }
        }

        //webKitView.scroll(NSPoint.init(x: 0, y: 0))
        
        if(clipboardItems.count > 0){
            webKitView.mainFrameURL = "https://translate.google.com/m/translate#en/ar/\(clipboardItems[0])"
        }else{
            webKitView.mainFrameURL = "https://translate.google.com/m/translate#en/ar/"
        }
    }
    
  func updateQuote() {
    textLabel.stringValue = String(describing: quotes[currentQuoteIndex])
  }

  override func viewWillAppear() {
    super.viewWillAppear()

    currentQuoteIndex = 0
  }
}

// MARK: Actions

extension QuotesViewController {
  @IBAction func goLeft(_ sender: NSButton) {
    currentQuoteIndex = (currentQuoteIndex - 1 + quotes.count) % quotes.count
  }

  @IBAction func goRight(_ sender: NSButton) {
    currentQuoteIndex = (currentQuoteIndex + 1) % quotes.count
  }

  @IBAction func quit(_ sender: NSButton) {
    NSApplication.shared().terminate(sender)
  }
}

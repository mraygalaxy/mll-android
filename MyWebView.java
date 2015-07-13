package org.renpy.android;

import android.webkit.WebView;
import android.app.Activity;
import android.view.KeyEvent;
import android.util.Log;
import android.content.Context;
 
public class MyWebView extends WebView {
     
    public MyWebView(Context context) {
        super(context);
        Log.d("MICA", "MyWebview: Initialized MyWebView");
    }

    public boolean onKeyUp(int keyCode, KeyEvent event) {
        Log.d("MICA", "MyWebView keyup got: " + keyCode);
        return false;
    }

    public boolean onKeyDown(int keyCode, KeyEvent event) {
        Log.d("MICA", "MyWebView keydown got: " + keyCode);
        return false;
    }
 
}

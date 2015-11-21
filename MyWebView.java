package org.renpy.android;

import android.webkit.WebView;
import android.app.Activity;
import android.view.KeyEvent;
import android.util.Log;
import android.content.Context;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.BaseInputConnection;
import android.view.inputmethod.InputConnection;
 
public class MyWebView extends WebView {
     
    public MyWebView(Context context) {
        super(context);
        Log.d("MICA", "MyWebview: Initialized MyWebView");
    }

    @Override
    public InputConnection onCreateInputConnection(EditorInfo outAttrs) {
        return new BaseInputConnection(this, false); //this is needed for #dispatchKeyEvent() to be notified.
    }

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        boolean dispatchFirst = super.dispatchKeyEvent(event);
	int keyCode = event.getKeyCode();
        if (event.getAction() == KeyEvent.ACTION_UP) {
            switch (keyCode) {
                case KeyEvent.KEYCODE_ENTER:
		    Log.d("MICA", "MyWebView ENTER key!");
		    //loadUrl("javascript: chatEnter();");
                    break;
            }
	}
        return dispatchFirst;
    }
 
}

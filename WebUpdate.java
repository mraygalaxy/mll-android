package org.renpy.android;

import android.app.Service;
import android.app.Activity;
import android.content.Context;
import android.support.v4.content.LocalBroadcastManager;
import android.content.BroadcastReceiver;
import android.webkit.WebView;
import android.content.Intent;
import android.content.IntentFilter;
import java.lang.Runnable;
 
public class WebUpdate {
     
    private Context _context;
    private Activity _activity;
    private Service _service;
    private WebView webview = null;
    private BroadcastReceiver mMessageReceiver = null;
     
    public WebUpdate(Service service){
        System.out.println("MICA WebUpdate: Will generate WebUpdate events from service.");
        this._service = service;
        this._context = service.getApplicationContext();
    }

    public void send(String message) {
         Intent intent = new Intent("mica-webview-update");
	 intent.putExtra("message", message);
	 LocalBroadcastManager.getInstance(this._context).sendBroadcast(intent);
    }

    public WebUpdate(Activity activity, WebView wv){
        System.out.println("MICA WebUpdate: Will process WebUpdate on webview.");
        this._context = activity.getApplicationContext();
        this.webview = wv;
        this._activity = activity;

        mMessageReceiver = new BroadcastReceiver() {
	  @Override
	  public void onReceive(Context context, Intent intent) {
	    // Get extra data included in the Intent
	    final String message = intent.getStringExtra("message");
	    System.out.println("MICA WebUpdate: Got message: " + message);
            _activity.runOnUiThread(new Runnable() { 
                public void run() {
                    webview.loadUrl(message);
                }
            });
	  }
	};

        LocalBroadcastManager.getInstance(this._context).registerReceiver(mMessageReceiver, new IntentFilter("mica-webview-update"));
    }
}

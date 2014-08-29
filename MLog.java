package org.renpy.android;

import android.util.Log;
import android.app.Activity;
import android.content.Context;
 
public class MLog {
     
    private Context _context;
     
    public MLog(Activity activity){
        Log.d("MICA", "MLog logging class initialized.");
        this._context = activity.getApplicationContext();
    }
 
    public void debug(String msg){
        Log.d("MICA", msg);
    }
    public void info(String msg){
        Log.i("MICA", msg);
    }
    public void warn(String msg){
        Log.w("MICA", msg);
    }
    public void err(String msg){
        Log.e("MICA", msg);
    }
    public void error(String msg) {
        err(msg);
    }
}

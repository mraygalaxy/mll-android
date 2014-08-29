package org.renpy.android;

import android.app.Activity;
import android.content.Context;
 
public class MLog {
     
    private Context _context;
     
    public MLog(Activity activity){
        System.out.println("MLog logging class initialized.");
        this._context = activity.getApplicationContext();
    }
 
    public void debug(String msg){
        System.out.println("MICA DEBUG: " + msg);
    }
    public void info(String msg){
        System.out.println("MICA INFO: " + msg);
    }
    public void warn(String msg){
        System.out.println("MICA WARN: " + msg);
    }
    public void err(String msg){
        System.out.println("MICA ERROR: " + msg);
    }
    public void error(String msg) {
        err(msg);
    }
}

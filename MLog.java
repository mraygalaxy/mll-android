package org.renpy.android;

import android.app.Service;
import android.content.Context;
 
public class MLog {
     
    private Context _context;
     
    public MLog(Service service){
        System.out.println("MLog connectivity class initialized.");
        this._context = service.getApplicationContext();
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
}

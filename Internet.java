package org.renpy.android;

import android.app.Service;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
 
public class Internet {
     
    private Context _context;
     
    public Internet(Service service){
        System.out.println("INTERNET: Internet connectivity class initialized.");
        this._context = service.getApplicationContext();
    }
 
    public boolean connected(){
        boolean online = false;
        boolean expensive = false;
        ConnectivityManager connectivity = (ConnectivityManager) _context.getSystemService(Context.CONNECTIVITY_SERVICE);
        System.out.println("INTERNET: CHECKING CONNECTIVITY");
          if (connectivity != null) 
          {
              NetworkInfo[] info = connectivity.getAllNetworkInfo();
              if (info != null) 
                  for (int i = 0; i < info.length; i++) 
                      if (info[i].getState() == NetworkInfo.State.CONNECTED)
                      {
                            System.out.println("INTERNET: Yes, we are connected: type: " + info[i].getTypeName() + " (" + info[i].getType() + ")");
                            if(info[i].getType() == ConnectivityManager.TYPE_MOBILE) {
                                System.out.println("INTERNET: We're on MOBILE: Recommend disabling replication.");
                                expensive = true;
                            }
                            online = true;
                      }
 
          }
                
          if (!online) {
              System.out.println("INTERNET: No, we are offline.");
          }
          return online;
    }
}

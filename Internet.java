package org.renpy.android;

import android.app.Activity;
import android.util.Log;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
 
public class Internet {
     
    private Context _context;
     
    public Internet(Activity activity){
        Log.d("MICA", "INTERNET: Internet connectivity class initialized.");
        this._context = activity.getApplicationContext();
    }
 
    public String connected(){
        boolean online = false;
        boolean expensive = false;
        ConnectivityManager connectivity = (ConnectivityManager) _context.getSystemService(Context.CONNECTIVITY_SERVICE);
        Log.d("MICA", "INTERNET: CHECKING CONNECTIVITY");
          if (connectivity != null) 
          {
              NetworkInfo[] info = connectivity.getAllNetworkInfo();
              if (info != null) 
                  for (int i = 0; i < info.length; i++) 
                      if (info[i].getState() == NetworkInfo.State.CONNECTED || info[i].getState() == NetworkInfo.State.CONNECTING)
                      {
                            Log.d("MICA", "INTERNET: Yes, we are connected: type: " + info[i].getTypeName() + " (" + info[i].getType() + ")");
                            if(info[i].getType() == ConnectivityManager.TYPE_MOBILE) {
                                Log.d("MICA", "INTERNET: We're on MOBILE: Recommend disabling replication.");
                                expensive = true;
                            }
                            online = true;
                      }
                        /*
                        else {
                            System.out.println("INTERNET: No, we are not connected: type: " + info[i].getTypeName() + " (" + info[i].getType() + ")");
                      }
                        */
 
          }
                
          if (!online) {
              Log.d("MICA", "INTERNET: No, we are offline.");
          }

          if (online) {
                if (expensive) {
                        return "expensive";
                } else {
                        return "online";
                }
          }
          return "none";
    }
}

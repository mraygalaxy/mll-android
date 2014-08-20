/*
 * This is a class which MICA interfaces with from Python via the pyjnius/python-for-android projects.
 * 
 * It exposes the native Couchbase-Lite mobile API directly in Python,
 * as well as activate couchbase-Lite replication between the mobile application and server.
 *
 */

package org.renpy.android;

import org.renpy.android.Internet;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.content.BroadcastReceiver;
import android.app.Service;
import android.content.res.AssetManager;

import com.couchbase.lite.Context;
import com.couchbase.lite.android.AndroidNetworkReachabilityManager;
import com.couchbase.lite.NetworkReachabilityManager;
import com.couchbase.lite.CouchbaseLiteException;
import com.couchbase.lite.Database;
import com.couchbase.lite.Manager;
import com.couchbase.lite.View;
import com.couchbase.lite.Status;
import com.couchbase.lite.Revision;
import com.couchbase.lite.Attachment;
import com.couchbase.lite.Query;
import com.couchbase.lite.QueryRow;
import com.couchbase.lite.QueryEnumerator;
import com.couchbase.lite.android.AndroidContext;
import com.couchbase.lite.javascript.JavaScriptViewCompiler;
import com.couchbase.lite.listener.Credentials;
import com.couchbase.lite.listener.LiteListener;
import com.couchbase.lite.replicator.Replication;
import com.couchbase.lite.auth.Authenticator;
import com.couchbase.lite.auth.AuthenticatorFactory;
import com.couchbase.lite.auth.BasicAuthenticator;
import com.couchbase.lite.support.CouchbaseLiteHttpClientFactory;
import com.couchbase.lite.support.HttpClientFactory;
import com.couchbase.lite.support.PersistentCookieStore;
import com.couchbase.lite.router.Router;
import com.couchbase.lite.util.Log;
import com.couchbase.lite.Document;
import com.couchbase.lite.UnsavedRevision;
import com.couchbase.lite.internal.RevisionInternal;
import com.couchbase.lite.Database.TDContentOptions;
import com.couchbase.lite.Mapper;
import com.couchbase.lite.Reducer;
import com.couchbase.lite.View.TDViewCollation;

import java.io.File;
import java.io.IOException;
import java.io.PushbackInputStream;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.EnumSet;
import java.util.Iterator;
import java.util.zip.GZIPInputStream;
import java.net.URL;
import java.net.MalformedURLException;
import java.io.InputStream;
import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.security.KeyStore;
import java.security.NoSuchAlgorithmException;
import java.security.cert.Certificate;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.security.cert.CertificateFactory;
import java.security.KeyStoreException;
import java.security.KeyManagementException;
import java.security.UnrecoverableKeyException;
import java.lang.InterruptedException;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import javax.net.ssl.SSLContext;
import java.net.Socket;
import java.net.UnknownHostException;

import org.apache.http.conn.ssl.SSLSocketFactory;
import org.apache.commons.io.IOUtils;

import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.map.annotate.JsonSerialize.Inclusion;
import org.codehaus.jackson.type.TypeReference;

public class Couch {

    private static final int DEFAULT_LISTEN_PORT = 5984;

    public static String TAG = "COUCHBASE: ";
    private Manager manager;
    private android.content.Context context;
    private LiteListener listener = null;
    private Thread listenerThread;
    private HashMap<String, Object> dbs;
    private HashMap<String, Object> pulls;
    private HashMap<String, Object> pushes;
    private HashMap<String, Object> urls;
    private HashMap<String, Object> seeds;
    String cert_path = null;
    Service mService = null;
    private BroadcastReceiver wifi_receiver;
    private Internet in;
    

    public class MySSLSocketFactory extends SSLSocketFactory {
         SSLContext sslContext = SSLContext.getInstance("TLS");

         public MySSLSocketFactory(KeyStore truststore) throws NoSuchAlgorithmException, KeyManagementException, KeyStoreException, UnrecoverableKeyException {
             super(truststore);

             TrustManager tm = new X509TrustManager() {
                 public void checkClientTrusted(X509Certificate[] chain, String authType) throws CertificateException {
                 }

                 public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {
                 }

                 public X509Certificate[] getAcceptedIssuers() {
                     return null;
                 }
             };

             sslContext.init(null, new TrustManager[] { tm }, null);
         }

         @Override
         public Socket createSocket(Socket socket, String host, int port, boolean autoClose) throws IOException, UnknownHostException {
             return sslContext.getSocketFactory().createSocket(socket, host, port, autoClose);
         }

         @Override
         public Socket createSocket() throws IOException {
             return sslContext.getSocketFactory().createSocket();
         }

         public String[] getDefaultCipherSuites() {
            return sslContext.getSocketFactory().getSupportedCipherSuites();
         }
         public String[] getSupportedCipherSuites() {
            return sslContext.getSocketFactory().getSupportedCipherSuites();
         }

        public Socket createSocket(String s, int i) throws IOException {
            return sslContext.getSocketFactory().createSocket(s, i);
        }
    }
 
    private void initializeSecurity(CouchbaseLiteHttpClientFactory factory) throws IOException, CertificateException, KeyStoreException, NoSuchAlgorithmException, KeyManagementException, InterruptedException, UnrecoverableKeyException {
        AssetManager am = mService.getAssets();
        InputStream is = IOUtils.toInputStream(cert_path, "UTF-8");
        // Load CAs from an InputStream
        CertificateFactory cf = CertificateFactory.getInstance("X.509");
        InputStream caInput = new BufferedInputStream(is);
        Certificate ca;
        try {
            ca = cf.generateCertificate(caInput);
        } finally {
            caInput.close();
        }
        // Create a KeyStore containing our trusted CAs
        String keyStoreType = KeyStore.getDefaultType();
        KeyStore keyStore = KeyStore.getInstance(keyStoreType);
        keyStore.load(null, null);
        keyStore.setCertificateEntry("ca", ca);
        SSLSocketFactory sf = new MySSLSocketFactory(keyStore);
        factory.setSSLSocketFactory(sf);
    }


    public class MicaContext extends AndroidContext {

        private android.content.Context wrapped;

        public MicaContext(android.content.Context wrapped) {
            super(wrapped);
            this.wrapped = wrapped;
        }

        @Override
        public File getFilesDir() {
            return wrapped.getExternalFilesDir(null);
        }
    }

    public Couch(String username, String password, int suggestedListenPort, String cert, Service service) throws IOException {
        try {
            dbs = new HashMap<String, Object>();
            pulls = new HashMap<String, Object>();
            pushes = new HashMap<String, Object>();
            seeds = new HashMap<String, Object>();
            urls = new HashMap<String, Object>();
	    mService = service;
            System.out.println(TAG + "Trying to get application context.");
            context = mService.getApplicationContext();
            System.out.println(TAG + "Trying to get build android context.");
            MicaContext mc = new MicaContext(context);
            System.out.println(TAG + "Trying to make manager.");
            Manager.enableLogging(Log.TAG, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_SYNC, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_QUERY, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_VIEW, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_DATABASE, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_REMOTE_REQUEST, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_ROUTER, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_LISTENER, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_MULTI_STREAM_WRITER, Log.VERBOSE);
            Manager.enableLogging(Log.TAG_BLOB_STORE, Log.VERBOSE);
            manager = new Manager(mc, Manager.DEFAULT_OPTIONS);
            System.out.println(TAG + "Trying to set compiler.");
            View.setCompiler(new JavaScriptViewCompiler());
            System.out.println(TAG + "Manager stores database here: " + manager.getDirectory());
            System.out.println(TAG + "Listing databases.");
            for (String dbname : manager.getAllDatabaseNames()) {
                System.out.println(TAG + "Manager has databases: " + dbname);
            }
            System.out.println(TAG + "Finished listing databases.");

	    System.out.println(TAG + "Trying to start listener on port: " + suggestedListenPort);
	    Credentials creds = new Credentials(username, password);
	    listener = new LiteListener(manager, suggestedListenPort, creds);
	    listenerThread = new Thread(listener);
	    listenerThread.start();
	    cert_path = cert;

	    wifi_receiver = new BroadcastReceiver()
		{
			 @Override
			 public void onReceive(android.content.Context context, Intent intent) {
				  int extraWifiState = intent.getIntExtra(WifiManager.EXTRA_WIFI_STATE ,
				    WifiManager.WIFI_STATE_UNKNOWN);
				 
				  switch(extraWifiState){
					  case WifiManager.WIFI_STATE_DISABLED:
					    System.out.println(TAG + "Wifi disabled.");
					    changeAllReplications(false);
					   break;
					  case WifiManager.WIFI_STATE_DISABLING:
					    System.out.println(TAG + "Wifi disabling.");
					   break;
					  case WifiManager.WIFI_STATE_ENABLED:
					    System.out.println(TAG + "Wifi enabled.");
					    changeAllReplications(true);
					   break;
					  case WifiManager.WIFI_STATE_ENABLING:
					    System.out.println(TAG + "Wifi enabling.");
					   break;
					  case WifiManager.WIFI_STATE_UNKNOWN:
					    System.out.println(TAG + "Wifi unknown.");
					   break;
				  }
	 
			}
		};

            mService.registerReceiver(wifi_receiver, new IntentFilter(WifiManager.WIFI_STATE_CHANGED_ACTION));

	    in = new Internet(mService);

        } catch (Exception e) {
		dumpError(e);
        }
    }

    private void changeAllReplications(boolean start) {
	try {
		    Iterator it = urls.entrySet().iterator();
		    while (it.hasNext()) {
			Map.Entry pairs = (Map.Entry)it.next();
			String database_name = (String) pairs.getKey();
			String url = (String) pairs.getValue();
			
			if (start) {
			    System.out.println(TAG + "Starting replication for DB: " + database_name);
		            replicate(database_name, url, true);
			} else {
			    System.out.println(TAG + "Stopping replication for DB: " + database_name);
			    stop_replication(database_name);
			}
		    }
		    System.out.println(TAG + "Change all replications exiting.");
		    
        } catch (Exception e) {
		dumpError(e);
        }
    }

    public boolean exists(String database_name) throws CouchbaseLiteException {
	return manager.getExistingDatabase(database_name) != null;
    }

    public int start(String database_name) throws IOException, CouchbaseLiteException {
        try {
                if (dbs.get(database_name) == null) {
                    System.out.println(TAG + "Trying to open database: " + database_name);
                    Database database = manager.getDatabase(database_name);
                    database.open();
                    dbs.put(database_name, database);	

                    PersistentCookieStore cookieStore = database.getPersistentCookieStore();
                    CouchbaseLiteHttpClientFactory htf = new CouchbaseLiteHttpClientFactory(cookieStore);
                    manager.setDefaultHttpClientFactory(htf);
                    initializeSecurity(htf);
                }

		System.out.println(TAG + "We're ready to go!");
		return listener.getListenPort();
        } catch (Exception e) {
		dumpError(e);
        }

	return -1;
    }

    public void stop_replication(String database_name) {
	if (pushes.get(database_name) != null) {
	     Replication push = (Replication) pushes.remove(database_name);
	     push.stop();
             System.out.println(TAG + "Stopped push replication.");
        }

	if (pulls.get(database_name) != null) {
	     Replication pull = (Replication) pulls.remove(database_name);
	     pull.stop();
             System.out.println(TAG + "Stopped pull replication.");
        }
    }

    public String compact(String database_name) throws CouchbaseLiteException {
	if (dbs.get(database_name) != null) {
             System.out.println(TAG + "Compacting database: " + database_name);
	     Database db = (Database) dbs.get(database_name);
	     db.compact();
             System.out.println(TAG + "Compaction finished: " + database_name);
	}
	
	return "";
    }

    public void drop(String database_name) throws CouchbaseLiteException {
        stop_replication(database_name);

	if (dbs.get(database_name) != null) {
	     Database db = (Database) dbs.remove(database_name);
	     db.delete();
             System.out.println(TAG + "Deleted database: " + database_name);
	}
    }

    public void stop(String database_name) {
	stop_replication(database_name);

	if (dbs.get(database_name) != null) {
	     Database db = (Database) dbs.remove(database_name);
	    /* 
	     * The CBL api doesn't have a 'close' database (nor in the manager).
	     * At least, I couldn't find it in the documentation.
	     */
	     //db.close();
             System.out.println(TAG + "Closed database: " + database_name);
	}
    }

    public int replicate(String database_name, String server, boolean force) {
	if (pushes.get(database_name) != null || pulls.get(database_name) != null) {
            System.out.println(TAG + "Database " + database_name + " is already replicating.");
	    return 0;
	}
        URL url;
        try {
            url = new URL(server + "/" + database_name);
        } catch (MalformedURLException e) {
            System.out.println(TAG + "Your replication URL is not good: " + e);
            return -1;
        }
        System.out.println(TAG + "creating replicator");

	if (urls.get(database_name) == null) {
		urls.put(database_name, server);
	}

	String conn = in.connected();
	
	if (in.connected() == "expensive") {
		System.out.println(TAG + "Not going to start replication on 3G =(");
		return 0;
	} else if(force || conn == "online") {
		System.out.println(TAG + "Starting replication!");
	} else {
		System.out.println(TAG + "No internet. Not starting replication.");
		return 0;
        }

        Database database = (Database) dbs.get(database_name);
        Replication pull = database.createPullReplication(url);
        Replication push = database.createPushReplication(url);
        pull.setContinuous(true);
        push.setContinuous(true);

        System.out.println(TAG + "Setting change listeners for replication");

        pull.addChangeListener(new Replication.ChangeListener() {
            @Override
            public void changed(Replication.ChangeEvent event) {
                System.out.println(TAG + "Pull Replication status changed: " + event); 
                Replication replication = event.getSource();
                if (!replication.isRunning()) {
                    System.out.println(TAG + " replicator " + replication + " is not running");
                }
                else {
                    int processed = replication.getCompletedChangesCount();
                    int total = replication.getChangesCount();
                    System.out.println(TAG + "Pull Replicator processed " + processed + " / " + total);
                }
            }
        });

        push.addChangeListener(new Replication.ChangeListener() {
            @Override
            public void changed(Replication.ChangeEvent event) {
                System.out.println(TAG + "Push Replication status changed: " + event); 
                Replication replication = event.getSource();
                if (!replication.isRunning()) {
                    System.out.println(TAG + " replicator " + replication + " is not running");
                }
                else {
                    int processed = replication.getCompletedChangesCount();
                    int total = replication.getChangesCount();
                    System.out.println(TAG + "Push Replicator processed " + processed + " / " + total);
                }
            }
        });

	pull.start();
	push.start();
        pulls.put(database_name, pull);
        pushes.put(database_name, push);

        return 0;
    }

    private void dumpError(Exception e) {
	System.out.println(TAG + "Error in Mica: " + e);
	System.out.println(TAG + e.getMessage());
	System.out.println(TAG + e.getLocalizedMessage());
	System.out.println(TAG + e.getCause());
	System.out.println(TAG + Arrays.toString(e.getStackTrace()));
	e.printStackTrace();
    }

    private Map<String,Object> toJava(String json) throws IOException {
        return Manager.getObjectMapper().readValue(json, Map.class);
    }

    private String toJSON(Map<String,Object> objs) throws IOException {
        return Manager.getObjectMapper().writeValueAsString(objs);
    }

    public String put(String dbname, String name, String json) {
        try {
	    
            Database database = (Database) dbs.get(dbname);
            Document document = database.getDocument(name);
	    System.out.println(TAG + "Want to put to key " + name + " with a length: " + json.length());
            Map<String, Object> properties = toJava(json);
	    document.putProperties(properties);
	    System.out.println(TAG + "Revision committed for key " + name);
            return "";
        } catch(Exception e) {
            dumpError(e);
            return Arrays.toString(e.getStackTrace());
        }
    }

    public String get(String dbname, String name) {
        try {
            Database database = (Database) dbs.get(dbname);
            Document doc = database.getExistingDocument(name);
            if (doc == null) {
                    return "";
            } 
            return toJSON(doc.getProperties());
        } catch(Exception e) {
            dumpError(e);
            return null;
        }
    }

    public String delete(String dbname, String name) {
        try {
            Database database = (Database) dbs.get(dbname);
            Document doc = database.getExistingDocument(name);
            if (doc == null) {
                    return "Failure. Document does not exist.";
            } 
            doc.delete(); 
            return "";
        } catch(Exception e) {
            dumpError(e);
            return Arrays.toString(e.getStackTrace());
        }
    }

    public static InputStream decompressStream(InputStream input) throws IOException {
         PushbackInputStream pb = new PushbackInputStream( input, 2 );
         byte [] signature = new byte[2];
         pb.read( signature );
         pb.unread( signature );
         if( signature[ 0 ] == (byte) 0x1f && signature[ 1 ] == (byte) 0x8b )  {
            System.out.println(TAG + "Attachment is compressed. Need to decompress it first.");
           return new GZIPInputStream( pb );
         } else {
           return pb;
         }
    }

    public byte[] get_attachment(String dbname, String name, String filename) throws IOException {
        try {
            Database database = (Database) dbs.get(dbname);
            Document doc = database.getExistingDocument(name);
            //System.out.println(TAG + "Looking up attachment from document: " + name + " named " + filename);
            if (doc == null) {
                System.out.println(TAG + "No such document: " + name + ". Cannot get attachment.");
                return null;
            } 

            Revision rev = doc.getCurrentRevision();
            Attachment att = rev.getAttachment(filename);
            if (att == null) {
                System.out.println(TAG + "Document: " + name + " has no such attachment: " + filename);
            }

            InputStream is = decompressStream(att.getContent());
            byte[] result;
            //if (att.getGZipped()) // doesn't work
            /* couchdb is lying. use magic number method later. I filed a bug on github. No response yet. */

            result = IOUtils.toByteArray(is);
            //System.out.println(TAG + "Got " + result.length + " bytes.");
            return result;
        } catch(Exception e) {
            dumpError(e);
            return null;
        }
    }

    public String doc_exist(String dbname, String name) {
        try {
            Database database = (Database) dbs.get(dbname);
            Document doc = database.getExistingDocument(name);
            if (doc == null) {
                    return "false";
            } 
            return "true";
        } catch(Exception e) {
            dumpError(e);
            return "error";
        }
    }

    private View compileView(Database db, String viewName, Map<String,Object> viewProps) {
        System.out.println(TAG + "Recompiling view.");
        String language = (String)viewProps.get("language");
        if(language == null) {
            language = "javascript";
        }
        String mapSource = (String)viewProps.get("map");
        if(mapSource == null) {
            return null;
        }
        Mapper mapBlock = View.getCompiler().compileMap(mapSource, language);
        if(mapBlock == null) {
            Log.w(Log.TAG_ROUTER, "View %s has unknown map function: %s", viewName, mapSource);
            return null;
        }
        String reduceSource = (String)viewProps.get("reduce");
        Reducer reduceBlock = null;
        if(reduceSource != null) {
            System.out.println(TAG + "Recompiling view's reducer as well.");
            reduceBlock = View.getCompiler().compileReduce(reduceSource, language);
            if(reduceBlock == null) {
                Log.w(Log.TAG_ROUTER, "View %s has unknown reduce function: %s", viewName, reduceBlock);
                return null;
            }
        } else {
            //System.out.println(TAG + "View has no reducer. Skipping.");
        }

        View view = db.getView(viewName);
        view.setMapReduce(mapBlock, reduceBlock, "1");

        if (reduceSource != null) {
             //System.out.println(TAG + "Asserting view " + viewName + " got its reducer.");
             assert(view.getReduce() != null);
        }

        String collation = (String)viewProps.get("collation");


        if("raw".equals(collation)) {
            view.setCollation(TDViewCollation.TDViewCollationRaw);
        }

        return view;
    }


    private Status queryDesignDoc(Database db, String designDoc, String viewName, boolean force) throws CouchbaseLiteException {
        String tdViewName = String.format("%s/%s", designDoc, viewName);
        View view = db.getExistingView(tdViewName);
        if(force || view == null || view.getMap() == null) {
            // No TouchDB view is defined, or it hasn't had a map block assigned;
            // see if there's a CouchDB view definition we can compile:
            RevisionInternal rev = db.getDocumentWithIDAndRev(String.format("_design/%s", designDoc), null, EnumSet.noneOf(TDContentOptions.class));
            if(rev == null) {
                return new Status(Status.NOT_FOUND);
            }
            Map<String,Object> views = (Map<String,Object>)rev.getProperties().get("views");
            Map<String,Object> viewProps = (Map<String,Object>)views.get(viewName);
            if(viewProps == null) {
                return new Status(Status.NOT_FOUND);
            }
            // If there is a CouchDB view, see if it can be compiled from source:
            view = compileView(db, tdViewName, viewProps);
            if(view == null) {
                return new Status(Status.INTERNAL_SERVER_ERROR);
            }
        }

        view.updateIndex();

        return new Status(Status.OK);
    }

    public void view_seed(String uuid, String username, String key_value) {
//    public void view_seed(String uuid, String key_value) {
        if(seeds.get(uuid) == null) {
            //System.out.println(TAG + "New set of seeds for uuid " + uuid + ", example: " + key_value);
            List<Object> keylist = new ArrayList<Object>();
            seeds.put(uuid, keylist);
        }
//        ((List<Object>) seeds.get(uuid)).add(key_value);
        List<String> keypair = new ArrayList<String>();
        keypair.add(username);
        keypair.add(key_value);
        ((List<Object>) seeds.get(uuid)).add(keypair);
    }

    public void view_seed_cleanup(String uuid) {
        if(seeds.get(uuid) != null) {
            //System.out.println(TAG + "Flushing seed keys for uuid " + uuid);
            seeds.remove(uuid);
        } 
	//System.out.println(TAG + "Total views in progress: " + seeds.size());
    }

    private View rebuildView(Database database, String designDoc, String viewName, boolean force) throws CouchbaseLiteException {
	View v = null;
        String name = designDoc + "/" + viewName;
	int status = queryDesignDoc(database, designDoc, viewName, force).getCode();
	if (status == Status.OK) {
	    System.out.println(TAG + "View pulled in from disk " + name + ".");
	    v = database.getExistingView(name);
	    assert(v != null);
	    assert(v.getViewId() > 0);
	} else {
	    System.out.println(TAG + "Could not pull in view from disk: " + status);
	    return null;
	}

	return v;
    }
    public Iterator<QueryRow> view(String dbname, String designDoc, String viewName, String parameters, String username) {
//    public Iterator<QueryRow> view(String dbname, String designDoc, String viewName, String parameters) {
        try {
            Database database = (Database) dbs.get(dbname);
            String name = designDoc + "/" + viewName;
            View v = database.getExistingView(name);

            if (v == null) {
                System.out.println(TAG + "view " + name + " not found. =(");
		v = rebuildView(database, designDoc, viewName, false);
		if (v == null) {
		    return null;
	        }
            }

            //System.out.println(TAG + "View found: " + name);

            if (v.isStale()) {
                System.out.println(TAG + "View is stale. Rebuilding and ReIndexing...");
		v = rebuildView(database, designDoc, viewName, true);
		if (v == null) {
		    return null;
	        }
                System.out.println(TAG + "Indexing complete.");
            }

            if (v.getReduce() == null) {
                RevisionInternal rev = database.getDocumentWithIDAndRev(String.format("_design/%s", designDoc), null, EnumSet.noneOf(TDContentOptions.class));
                Map<String,Object> views = (Map<String,Object>)rev.getProperties().get("views");
                Map<String,Object> viewProps = (Map<String,Object>)views.get(viewName);
                if (viewProps.get("reduce") != null) {
                    System.out.println(TAG + "Uh oh. This view really does have a reducer!!!. Couch is lying again. Need to file a bug.");
                    v = compileView(database, name, viewProps);
                    System.out.println(TAG + "OK. Asserting that the liar is smacked:");
                    assert(v.getReduce() != null);
                }
            }

            Query query = v.createQuery();

            if (parameters != null && parameters.length() > 0 && !(parameters.equals(""))) {
                //System.out.println(TAG + "Converting parameters to objects: length: " + parameters.length() + ", contents: *" + parameters + "*");
                Map<String, Object> properties = toJava(parameters);

                //System.out.println(TAG + "Storing parameters to query: " + toJSON(properties));

                if (properties.get("startkey") != null && properties.get("endkey") != null) {
                    //System.out.println(TAG + "Setting start and endkey");
                    query.setStartKey((List<Object>) properties.get("startkey"));
                    query.setEndKey((List<Object>) properties.get("endkey"));
                } else if(properties.get("keys") != null) {
                    String uuid = (String) properties.get("keys");
                    //System.out.println(TAG + "Setting seeds keys for uuid: " + uuid);
                    List<Object> keylist = (List<Object>) seeds.get(uuid);
                    assert(keylist != null);
                    seeds.remove(uuid);
                    query.setKeys(keylist);
                    //System.out.println(TAG + "Finished setting seeds keys for uuid: " + uuid);
                } else if(properties.get("stale") != null) {
                    System.out.println(TAG + "WARNING: View request 'stale' parameter not supported!");
                } 
            }
                
            //System.out.println(TAG + "Running query");
            QueryEnumerator rowEnum = query.run();

            //System.out.println(TAG + "Query complete. Extracting results.");

            if (rowEnum.getCount() > 0) {
                //System.out.println(TAG + "Returning final view results: " + rowEnum.getCount());
                return rowEnum;
            }

            return rowEnum;

        } catch(CouchbaseLiteException e) {
            dumpError(e);
            return null;
        } catch(Exception e) {
            dumpError(e);
            return null;
        }
    }

    public boolean view_has_next(Iterator<QueryRow> it) {
        assert(it != null);
        boolean has_next = it.hasNext();
	/*
        if (has_next) {
            System.out.println(TAG + "View iterator not exhausted yet.");
        } else {
            System.out.println(TAG + "View iterator is exhausted.");
        }
	*/
        return has_next;
    }

    public String view_next(Iterator<QueryRow> it) {
        assert(it != null);
        assert(it.hasNext());

        try {
            Map<String, Object> dict = new HashMap<String, Object>();
            Map<String, Object> result = new HashMap<String, Object>();
            QueryRow row = it.next();

            result.put("key", row.getKey());
            result.put("value", row.getValue());
            dict.put("result", result);

            return toJSON(dict);

        } catch(Exception e) {
            dumpError(e);
            return null;
        }
    }
 
}

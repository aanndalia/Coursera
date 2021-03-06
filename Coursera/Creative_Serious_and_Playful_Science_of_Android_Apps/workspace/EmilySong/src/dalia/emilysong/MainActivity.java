package dalia.emilysong;

import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.util.Log;

public class MainActivity extends Activity {

	MediaPlayer song;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //song = MediaPlayer.create(this, R.raw.yui_song);
        //song.start();
    }

    @Override
    protected void onResume() {
    	song = MediaPlayer.create(this, R.raw.yui_song);
    	song.start();
    	super.onResume();
    }
    
    @Override
    protected void onPause() {
    	song.stop();
    	song.release();
    	super.onPause();
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
    
    public void openNikushX(View v)
    {
    	//Log.d("DALIA", "In openNikushX");
    	String url = "http://www.nikushx.com";
    	Intent i = new Intent(Intent.ACTION_VIEW);
    	i.setData(Uri.parse(url));
    	startActivity(i);
    }
}

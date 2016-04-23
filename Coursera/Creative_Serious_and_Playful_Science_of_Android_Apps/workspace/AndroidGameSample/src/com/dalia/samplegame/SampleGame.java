package com.dalia.samplegame;

import com.dalia.framework.Screen;
import com.dalia.framework.implementation.AndroidGame;

public class SampleGame extends AndroidGame {
	@Override
	public Screen getInitScreen() {
		return new LoadingScreen(this);
	}
	
	@Override
	public void onBackPressed() {
		getCurrentScreen().backButton();
	}
}



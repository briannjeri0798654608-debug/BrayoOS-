#!/bin/bash
echo "⚡ Building BrayoOS Launcher..."

# Install build tools
pkg install -y gradle openjdk-17 aapt apksigner

# Create launcher project structure
mkdir -p ~/BrayoOS/phase3/apk/BrayoOSLauncher/{src,res,assets}
mkdir -p ~/BrayoOS/phase3/apk/BrayoOSLauncher/src/com/brayo/launcher
mkdir -p ~/BrayoOS/phase3/apk/BrayoOSLauncher/res/{layout,values,drawable}

# AndroidManifest.xml
cat > ~/BrayoOS/phase3/apk/BrayoOSLauncher/AndroidManifest.xml << 'MANEOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.brayo.launcher"
    android:versionCode="1"
    android:versionName="2.0">

    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
    <uses-permission android:name="android.permission.READ_CONTACTS"/>
    <uses-permission android:name="android.permission.CALL_PHONE"/>
    <uses-permission android:name="android.permission.READ_CALL_LOG"/>
    <uses-permission android:name="android.permission.SEND_SMS"/>
    <uses-permission android:name="android.permission.READ_SMS"/>
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.VIBRATE"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>

    <application
        android:label="BrayoOS"
        android:icon="@drawable/ic_launcher"
        android:theme="@style/BrayoTheme"
        android:allowBackup="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTask"
            android:stateNotNeeded="true"
            android:resumeWhilePausing="true"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.HOME"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <receiver android:name=".BootReceiver"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED"/>
            </intent-filter>
        </receiver>

    </application>
</manifest>
MANEOF

# Main Activity
cat > ~/BrayoOS/phase3/apk/BrayoOSLauncher/src/com/brayo/launcher/MainActivity.java << 'JAVAEOF'
package com.brayo.launcher;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.*;
import android.content.Intent;
import android.content.pm.*;
import android.graphics.Color;
import android.view.ViewGroup;
import java.util.List;

public class MainActivity extends Activity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Full screen dark theme
        getWindow().getDecorView().setBackgroundColor(
            Color.parseColor("#0D0D0D"));
        
        ScrollView scroll = new ScrollView(this);
        LinearLayout main = new LinearLayout(this);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setBackgroundColor(Color.parseColor("#0D0D0D"));
        
        // Header
        TextView header = new TextView(this);
        header.setText("⚡ BrayoOS v2.0");
        header.setTextColor(Color.parseColor("#00FF41"));
        header.setTextSize(24);
        header.setPadding(20, 40, 20, 10);
        main.addView(header);
        
        // ARIA Status
        TextView aria = new TextView(this);
        aria.setText("🤖 ARIA: Online | Built by Brayo & Claude");
        aria.setTextColor(Color.parseColor("#444444"));
        aria.setTextSize(12);
        aria.setPadding(20, 0, 20, 20);
        main.addView(aria);
        
        // App Grid
        GridView grid = new GridView(this);
        grid.setNumColumns(4);
        grid.setBackgroundColor(Color.parseColor("#0D0D0D"));
        
        // Load all apps
        PackageManager pm = getPackageManager();
        Intent intent = new Intent(Intent.ACTION_MAIN, null);
        intent.addCategory(Intent.CATEGORY_LAUNCHER);
        List<ResolveInfo> apps = pm.queryIntentActivities(
            intent, 0);
        
        AppAdapter adapter = new AppAdapter(this, apps);
        grid.setAdapter(adapter);
        
        grid.setOnItemClickListener((parent, view, pos, id) -> {
            ResolveInfo info = apps.get(pos);
            Intent launch = pm.getLaunchIntentForPackage(
                info.activityInfo.packageName);
            if (launch != null) startActivity(launch);
        });
        
        LinearLayout.LayoutParams params = 
            new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT);
        grid.setLayoutParams(params);
        main.addView(grid);
        scroll.addView(main);
        setContentView(scroll);
    }
}
JAVAEOF

# Boot Receiver
cat > ~/BrayoOS/phase3/apk/BrayoOSLauncher/src/com/brayo/launcher/BootReceiver.java << 'BOOTEOF'
package com.brayo.launcher;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class BootReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (Intent.ACTION_BOOT_COMPLETED.equals(
                intent.getAction())) {
            Intent launch = new Intent(context,
                MainActivity.class);
            launch.addFlags(
                Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(launch);
        }
    }
}
BOOTEOF

# Styles
cat > ~/BrayoOS/phase3/apk/BrayoOSLauncher/res/values/styles.xml << 'STYLEEOF'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="BrayoTheme" parent="android:Theme">
        <item name="android:windowBackground">#0D0D0D</item>
        <item name="android:colorBackground">#0D0D0D</item>
        <item name="android:textColor">#00FF41</item>
        <item name="android:colorPrimary">#00FF41</item>
        <item name="android:statusBarColor">#1A1A1A</item>
        <item name="android:navigationBarColor">#1A1A1A</item>
        <item name="android:windowFullscreen">false</item>
    </style>
</resources>
STYLEEOF

echo "✅ Launcher project created!"
echo "📁 Location: ~/BrayoOS/phase3/apk/BrayoOSLauncher"
echo "Next: Build with Sketchware Pro or Android Studio"

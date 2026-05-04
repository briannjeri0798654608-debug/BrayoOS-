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

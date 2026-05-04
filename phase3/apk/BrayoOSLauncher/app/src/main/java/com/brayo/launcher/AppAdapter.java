package com.brayo.launcher;

import android.content.*;
import android.content.pm.*;
import android.graphics.Color;
import android.view.*;
import android.widget.*;
import java.util.List;

public class AppAdapter extends BaseAdapter {
    private Context ctx;
    private List<ResolveInfo> apps;
    private PackageManager pm;

    public AppAdapter(Context ctx,
                     List<ResolveInfo> apps) {
        this.ctx = ctx;
        this.apps = apps;
        this.pm = ctx.getPackageManager();
    }

    @Override
    public int getCount() { return apps.size(); }

    @Override
    public Object getItem(int pos) {
        return apps.get(pos);
    }

    @Override
    public long getItemId(int pos) { return pos; }

    @Override
    public View getView(int pos, View convert,
                       ViewGroup parent) {
        LinearLayout layout = new LinearLayout(ctx);
        layout.setOrientation(
            LinearLayout.VERTICAL);
        layout.setGravity(android.view.Gravity.CENTER);
        layout.setPadding(5, 10, 5, 10);
        layout.setBackgroundColor(
            Color.parseColor("#1A1A1A"));

        ResolveInfo info = apps.get(pos);

        ImageView icon = new ImageView(ctx);
        icon.setImageDrawable(
            info.loadIcon(pm));
        icon.setLayoutParams(
            new LinearLayout.LayoutParams(80, 80));

        TextView name = new TextView(ctx);
        name.setText(info.loadLabel(pm));
        name.setTextColor(
            Color.parseColor("#00FF41"));
        name.setTextSize(9);
        name.setGravity(
            android.view.Gravity.CENTER);
        name.setMaxLines(1);

        layout.addView(icon);
        layout.addView(name);
        return layout;
    }
}

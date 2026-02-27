# Full App Integration Guidelines (Updated)

I see you already have a fantastic folder structure built! Let's just drop exactly what you have into the main application repository so everything hooks up smoothly to the dashboard. 

## 1. Where to drop the files

Move the items you already generated directly into your main project folder. 

Your final structure should look like this:

```text
ace-avionics-training-main/
├── dashboard.html             <-- Main Hub
├── course_index.json          <-- MASTER MAPPING (We just generated this)
├── shared/                    
│   ├── js/                      (ace-auth.js, supabase-client.js, etc.)
├── training_modules/          <-- 1. DROP YOUR TRAINING NODES HERE
│   ├── (Your node folders...)          
├── simulations/               <-- 2. DROP YOUR SIMULATIONS HERE
│   ├── (Your interactive simulations...)
└── script-backups/            <-- 3. DROP ALL YOUR PYTHON SCRIPTS HERE
    ├── generate_html_training.py
    └── replace_script...
```

**Note on Scripts:** The Python scripts do not run on the final website (Vercel only serves HTML/JS), but you should absolutely keep them safe in a folder inside the project (like `/script-backups/`) so you don't lose them! 

## 2. Integrating Content into the Gamification Tracking

For the `training_modules` and `simulations` to successfully award XP and grade readiness, the other agent just needs to make sure they include the Supabase client and fire a 'Completion Event' containing the correct `lo_id`.

### Add the Tracking Scripts
Any HTML page inside `training_modules` or `simulations` must include:
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="../shared/js/supabase-client.js"></script>
```

> [!WARNING]
> **Check Your Local Scripts:** The training node generator might output paths going up 3 levels (`../../../shared/js/supabase-client.js`). You MUST fix this to appropriately point to `../shared/js/supabase-client.js` depending on the directory depth where the file is dropped (e.g. `training_modules` is only 1 level deep).
>
> You also MUST fix the footer "Return to Portal" paths: Replace `href="index.html"` with `href="../index.html"` so it properly links to the main course page!

### Fire the Completion Event
When the user successfully reads the node, or successfully completes an interactive simulation (like the ESD bench), fire this event:

```javascript
if (window.AceSupabase && window.AceSupabase.trackQuestionEvent) {
  window.AceSupabase.trackQuestionEvent({
    lessonId: 'training-activity',      // e.g. 'training_modules' or 'simulations'
    questionId: 'unique-activity-id',   // Unique ID for the specific page/sim
    format: 'interactive',              // 'journey-read', 'interactive', 'quiz'
    loId: 'entry:q31',                  // CRITICAL: The LO ID this teaches (Must match course_index.json!)
    category: 'Safety',                 
    selectedIndex: 1,                   
    correctIndex: 1,                    
    isCorrect: true,                    // Triggered when they 'win' or complete the item
    points: 50                          // Nodes = 10xp, Simulations = 50xp
  });
}
```
If the other agent adds this script to the pages they generate, the student's progress will automatically sync to the Dashboard!

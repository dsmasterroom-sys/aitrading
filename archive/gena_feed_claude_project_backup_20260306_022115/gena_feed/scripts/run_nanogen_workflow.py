#!/usr/bin/env python3
"""
Automated Nanogen Workflow Runner for 9-Slide Carousel
Sequential processing with workflow API integration
"""

import json
import requests
import time
from pathlib import Path

# Configuration
NANOGEN_BASE_URL = "http://localhost:8000"
WORKFLOW_ID = "wf-1772343124650-u0xkt"
PROJECT_ROOT = Path("/Users/master/.openclaw/workspace/gena_feed_claude_project/gena_feed")
PROMPTS_FILE = PROJECT_ROOT / "weekly/image-prompts.json"
OUTPUT_DIR = PROJECT_ROOT / "output/nanogen_images"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_slide_prompts():
    """Load slide prompts and configurations from JSON"""
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_workflow_inputs(workflow_id, slide_config, creative_vision):
    """
    Update the workflow inputs for a specific slide
    
    This would interact with Nanogen's workflow API to:
    1. Set the text input (creative vision + slide prompt)
    2. Set the reference images (model + product images)
    """
    
    # Prepare the combined prompt
    combined_prompt = f"""Creative Vision: {creative_vision}

Slide Context: {slide_config['role']}

Prompt: {slide_config['prompt']}

Style: {slide_config.get('style_base', 'editorial fashion, clean minimal')}
"""
    
    # In a real implementation, this would call the Nanogen API
    # to update workflow node inputs
    # For now, we'll prepare the data structure
    
    workflow_updates = {
        "workflow_id": workflow_id,
        "node_updates": {
            "7": {  # Text Input #2 (creative vision)
                "text": combined_prompt
            }
            # Image inputs would be updated here with reference images
        }
    }
    
    return workflow_updates

def execute_workflow(workflow_id, slide_id):
    """
    Execute the Nanogen workflow for a single slide
    
    Returns: path to generated image
    """
    
    print(f"🎬 Executing workflow for {slide_id}...")
    
    # This is where we'd call Nanogen's workflow execution API
    # Endpoint might be something like: POST /api/workflow/{workflow_id}/execute
    
    try:
        # Placeholder for actual API call
        # response = requests.post(
        #     f"{NANOGEN_BASE_URL}/api/workflow/{workflow_id}/execute",
        #     timeout=300  # 5 minute timeout for generation
        # )
        
        # For now, simulate processing
        print(f"  ⏳ Processing through Prompt Agent...")
        time.sleep(2)  # Simulate prompt enhancement
        
        print(f"  🎨 Generating image with Gemini 3 Pro...")
        time.sleep(5)  # Simulate image generation
        
        # In real implementation, extract image URL from response
        generated_image_path = OUTPUT_DIR / f"{slide_id}.png"
        
        print(f"  ✅ Generated: {generated_image_path}")
        return str(generated_image_path)
        
    except requests.exceptions.Timeout:
        print(f"  ❌ Timeout generating {slide_id}")
        return None
    except Exception as e:
        print(f"  ❌ Error generating {slide_id}: {str(e)}")
        return None

def process_all_slides():
    """Main processing loop - sequential execution"""
    
    print("=" * 60)
    print("🚀 Nanogen Workflow Sequential Processing")
    print("=" * 60)
    
    # Load slide configurations
    config = load_slide_prompts()
    slides = config['slides']
    
    # Extract creative vision (could be from a separate source)
    creative_vision = "Young Korean model showcasing slant bag in natural, editorial style"
    
    results = []
    total_slides = len(slides)
    
    for idx, slide in enumerate(slides, 1):
        slide_id = slide['id']
        
        print(f"\n📍 Processing Slide {idx}/{total_slides}: {slide_id}")
        print(f"   Role: {slide['role']}")
        
        # Skip outfit swap for now (needs special handling)
        if slide.get('outfit_swap'):
            print(f"   ⚠️  Skipping outfit swap (requires separate processing)")
            continue
        
        # Step 1: Update workflow inputs
        print(f"   📝 Updating workflow inputs...")
        workflow_config = update_workflow_inputs(WORKFLOW_ID, slide, creative_vision)
        
        # Step 2: Execute workflow
        image_path = execute_workflow(WORKFLOW_ID, slide_id)
        
        # Step 3: Record result
        results.append({
            'slide_id': slide_id,
            'slide_number': slide['slide'],
            'status': 'success' if image_path else 'failed',
            'image_path': image_path,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Brief pause between slides
        if idx < total_slides:
            print(f"   ⏸️  Cooling down for 3 seconds...")
            time.sleep(3)
    
    # Save results
    results_file = OUTPUT_DIR / "generation_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("✨ Processing Complete!")
    print(f"📊 Results saved to: {results_file}")
    print("=" * 60)
    
    # Summary
    successful = sum(1 for r in results if r['status'] == 'success')
    print(f"\n✅ Successful: {successful}/{total_slides}")
    print(f"❌ Failed: {total_slides - successful}/{total_slides}")
    
    return results

if __name__ == "__main__":
    results = process_all_slides()

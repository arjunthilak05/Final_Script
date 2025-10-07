#!/usr/bin/env python3
"""
Test script for Station 15: Detailed Episode Outlining

This script tests the basic functionality of Station 15 agent including:
- Pydantic model validation
- Input/Output structure
- Model instantiation
"""

import sys
import asyncio
from pydantic import ValidationError

# Import Station 15 models and agent
from app.agents.station_15_detailed_episode_outlining import (
    Station15Input,
    SceneOutline,
    Station15Output,
    Station15DetailedEpisodeOutlining
)


def test_pydantic_models():
    """Test Pydantic model validation"""
    print("="*70)
    print("Testing Pydantic Models")
    print("="*70)
    
    # Test 1: Valid SceneOutline
    print("\n1. Testing SceneOutline with valid data...")
    try:
        scene = SceneOutline(
            scene_number=1,
            location="Test Location",
            time="Morning",
            characters_present=["Character A", "Character B"],
            goal_obstacle_choice_consequence="Character wants X but Y happens",
            reveal="Plant: Secret mentioned",
            soundscape_notes="Ambient sounds, footsteps",
            transition_to_next_scene="Fade to next scene",
            estimated_runtime="2 minutes"
        )
        print(f"   ✅ Valid SceneOutline created: Scene {scene.scene_number}")
    except ValidationError as e:
        print(f"   ❌ Validation failed: {e}")
        return False
    
    # Test 2: Invalid SceneOutline (missing required field)
    print("\n2. Testing SceneOutline with missing field (should fail)...")
    try:
        scene_invalid = SceneOutline(
            scene_number=1,
            location="Test Location",
            time="Morning"
            # Missing required fields
        )
        print(f"   ❌ Should have failed but didn't!")
        return False
    except ValidationError as e:
        print(f"   ✅ Correctly failed validation (expected behavior)")
    
    # Test 3: Valid Station15Input
    print("\n3. Testing Station15Input with valid data...")
    try:
        input_data = Station15Input(
            session_id="test_session",
            episode_number=1,
            blueprint_summary="Test summary of episode"
        )
        print(f"   ✅ Valid Station15Input created: Episode {input_data.episode_number}")
    except ValidationError as e:
        print(f"   ❌ Validation failed: {e}")
        return False
    
    # Test 4: Invalid Station15Input (negative episode number)
    print("\n4. Testing Station15Input with invalid episode_number (should fail)...")
    try:
        input_invalid = Station15Input(
            session_id="test_session",
            episode_number=0,  # Should be >= 1
            blueprint_summary="Test summary"
        )
        print(f"   ❌ Should have failed but didn't!")
        return False
    except ValidationError as e:
        print(f"   ✅ Correctly failed validation (expected behavior)")
    
    # Test 5: Valid Station15Output
    print("\n5. Testing Station15Output with valid data...")
    try:
        scenes = [
            SceneOutline(
                scene_number=1,
                location="Location 1",
                time="Morning",
                characters_present=["Character A"],
                goal_obstacle_choice_consequence="Goal and obstacle",
                reveal="None",
                soundscape_notes="Ambient sounds",
                transition_to_next_scene="Cut to next",
                estimated_runtime="2 minutes"
            ),
            SceneOutline(
                scene_number=2,
                location="Location 2",
                time="Afternoon",
                characters_present=["Character B", "Character C"],
                goal_obstacle_choice_consequence="Different goal",
                reveal="Plant: Something mentioned",
                soundscape_notes="Different sounds",
                transition_to_next_scene="Fade out",
                estimated_runtime="3 minutes"
            )
        ]
        
        output = Station15Output(
            episode_number=1,
            scenes=scenes
        )
        print(f"   ✅ Valid Station15Output created: {len(output.scenes)} scenes")
    except ValidationError as e:
        print(f"   ❌ Validation failed: {e}")
        return False
    
    # Test 6: JSON serialization
    print("\n6. Testing JSON serialization...")
    try:
        json_output = output.model_dump_json(indent=2)
        print(f"   ✅ JSON serialization successful ({len(json_output)} characters)")
        print(f"\n   Sample output (first 200 chars):")
        print(f"   {json_output[:200]}...")
    except Exception as e:
        print(f"   ❌ Serialization failed: {e}")
        return False
    
    # Test 7: JSON deserialization
    print("\n7. Testing JSON deserialization...")
    try:
        import json
        parsed = json.loads(json_output)
        reconstructed = Station15Output(**parsed)
        print(f"   ✅ JSON deserialization successful")
        print(f"      Episode: {reconstructed.episode_number}")
        print(f"      Scenes: {len(reconstructed.scenes)}")
    except Exception as e:
        print(f"   ❌ Deserialization failed: {e}")
        return False
    
    print("\n" + "="*70)
    print("✅ All Pydantic model tests passed!")
    print("="*70)
    return True


def test_agent_instantiation():
    """Test Station15DetailedEpisodeOutlining can be instantiated"""
    print("\n" + "="*70)
    print("Testing Station15DetailedEpisodeOutlining Instantiation")
    print("="*70)
    
    try:
        agent = Station15DetailedEpisodeOutlining(session_id="test_session")
        print(f"\n✅ Station15DetailedEpisodeOutlining instantiated successfully")
        print(f"   Session ID: {agent.session_id}")
        print(f"   Model: {agent.model_name}")
        print(f"   Station: {agent.station_name}")
        return True
    except Exception as e:
        print(f"\n❌ Agent instantiation failed: {e}")
        return False


def test_prompt_construction():
    """Test prompt construction without LLM call"""
    print("\n" + "="*70)
    print("Testing Prompt Construction")
    print("="*70)
    
    try:
        agent = Station15DetailedEpisodeOutlining(session_id="test_session")
        
        input_data = Station15Input(
            session_id="test_session",
            episode_number=1,
            blueprint_summary="Test episode summary for prompt construction"
        )
        
        context = {
            'project_bible': {'title': 'Test Project'},
            'character_bible': {'tier1_protagonists': []},
            'world_bible': {'geography': {'locations': []}},
            'reveal_matrix': {'reveals': []}
        }
        
        prompt = agent._construct_llm_prompt(input_data, context)
        
        print(f"\n✅ Prompt constructed successfully")
        print(f"   Length: {len(prompt)} characters")
        print(f"   Contains 'Episode Outline Builder': {'Yes' if 'Episode Outline Builder' in prompt else 'No'}")
        print(f"   Contains 'scene_number': {'Yes' if 'scene_number' in prompt else 'No'}")
        print(f"   Contains JSON format example: {'Yes' if 'episode_number' in prompt else 'No'}")
        
        print(f"\n   Sample prompt (first 500 chars):")
        print(f"   {prompt[:500]}...")
        
        return True
    except Exception as e:
        print(f"\n❌ Prompt construction failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("STATION 15 TEST SUITE")
    print("="*70)
    
    results = {
        'pydantic_models': test_pydantic_models(),
        'agent_instantiation': test_agent_instantiation(),
        'prompt_construction': test_prompt_construction()
    }
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! Station 15 is ready to use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


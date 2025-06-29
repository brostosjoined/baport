#!/usr/bin/env python3

"""Usage: port_7_to_8.py -f <plugin-name> -t <client/server type of mod>

You'll have to manually update the following:
From:
    with ba.Context(_ba.foreground_host_activity()):
To:
    with _ba.foreground_host_activity().context:
From:
    ba.Timer((POWERUP_WEAR_OFF_TIME - 2000),ba.WeakCall(self._multi_bomb_wear_off_flash),timeformat=ba.TimeFormat.MILLISECONDS)
To:
    ba.Timer((POWERUP_WEAR_OFF_TIME - 2000 / 1000),ba.WeakCall(self._multi_bomb_wear_off_flash))
From:
    ba.playsound(self._dingsound if importance == 1 else self._dingsoundhigh, volume=0.6)
To:
    self._dingsound.play(volume=0.6) if importance == 1 else self._dingsoundhigh.play(volume=0.6)
From:
    bui.app.ui_v1.use_toolbars
To:
    Either True or False, whatever works for you 
"""

import argparse
from pathlib import Path
import re

TRADEMARK = "# Porting made easier by baport.(https://github.com/bombsquad-community/baport)\n"

def detect_file_encoding(file_path) -> str|None:
    encodings = ['utf-8', 'latin-1', 'ascii', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'rb') as f:
                f.read().decode(encoding)
            return encoding
        except UnicodeDecodeError:
            pass
    return None

def api6_to_api8(content :str, plugin_type :str) -> str:
    """returns converted api 6/7 string data to api 9
    plugin_type is either client or server"""

    content = content.replace("# ba_meta require api 7", "# ba_meta require api 8")
    content = content.replace("# ba_meta export game", "# ba_meta export bascenev1.GameActivity")
    # Api 6 support
    content = content.replace("# ba_meta require api 6", "# ba_meta require api 8")
    content = content.replace("on_app_launch", "__init__")
    content = content.replace("ba._enums", "ba._generated.enums") 
    content = content.replace("get_account", "get_v1_account")                          
                    


    content = content.replace("user_agent_string", "legacy_user_agent_string")
    content = re.sub(r'^(import\s+[\w]+(\s*,\s*[\w]+)+)', lambda match: re.sub(r'\s*,\s*', '\nimport ', match.group()), content, flags=re.MULTILINE)
    content = content.replace("_ba.", "_babase.")
    content = content.replace("_ba.", "_babase.")
    content = content.replace("ba.", "babase.")
    content = content.replace("import _ba", "import _babase")
    content = content.replace("from ba import", "from babase import")
    content = content.replace("from _ba import", "from _babase import")
    content = re.sub(r'\bimport _ba\b', "import _babase", content)
    content = re.sub(r'\bimport ba(\b|\.(\w+))', "import babase\nimport bauiv1\nimport bascenev1", content)
    match = re.search(r'^(import\s+[\w]+(\s*,\s*[\w]+)*)', content, flags=re.MULTILINE)
    affected_methods = ["build_number", "device_name", "config_file_path", "version", "debug_build", "test_build", "data_directory", "python_directory_user", "python_directory_app", "python_directory_app_site", "api_version", "on_tv", "vr_mode","toolbar_test", "arcade_test", "headless_mode", "demo_mode", "protocol_version", "get_connection_to_host_info"]
    for word in affected_methods:
        if f".{word}" in content:
            first_import_index = match.start()
            content = content[:first_import_index] + 'from baenv import TARGET_BALLISTICA_BUILD as build_number\n' + content[first_import_index:]
            break
    content = content.replace("babase.app.ui", "bauiv1.app.ui_v1")
    content = content.replace("bauiv1.app.ui_v1.set_main_menu_window", "bauiv1.app.ui_v1.set_main_window")

    content = content.replace("babase.app.accounts_v1", "bauiv1.app.classic.accounts")

    ###################################################################################
    # Comment out one of these as per your requirements, depending whether to
    # stay local or if it'll also be needed to transmitted to the clients.

    ## For local:
    if plugin_type == "client":
        content = content.replace("_babase.screenmessage", "bauiv1.screenmessage")
        content = content.replace("babase.screenmessage", "bauiv1.screenmessage")
        content = content.replace("babase.getsound", "bauiv1.getsound")
        content = content.replace("_babase.gettexture", "bauiv1.gettexture")
        content = content.replace("babase.gettexture", "bauiv1.gettexture")
        content = content.replace("babase.getmesh", "bauiv1.getmesh")
        content = content.replace("babase.getcollisionmesh", "bauiv1.getcollisionmesh")
    else:
    ## For transmission:
        content = content.replace("_babase.screenmessage", "bascenev1.broadcastmessage")
        content = content.replace("babase.screenmessage", "bascenev1.broadcastmessage")
        content = content.replace("babase.getsound", "bascenev1.getsound")
        content = content.replace("_babase.gettexture", "bascenev1.gettexture")
        content = content.replace("babase.gettexture", "bascenev1.gettexture")
        content = content.replace("babase.getmesh", "bascenev1.getmesh")
        content = content.replace("babase.getcollisionmesh", "bascenev1.getcollisionmesh")
    ###################################################################################
    content = content.replace("babase.getcollidemesh", "bascenev1.getcollisionmesh")
    content = content.replace("collide_mesh", "collision_mesh")
    content = content.replace("babase.open_url", "bauiv1.open_url")
    content = content.replace("babase.IntSetting", "bascenev1.IntSetting")
    content = content.replace("babase.IntChoiceSetting", "bascenev1.IntChoiceSetting")
    content = content.replace("babase.FloatChoiceSetting", "bascenev1.FloatChoiceSetting")
    content = content.replace("babase.BoolSetting", "bascenev1.BoolSetting")
    content = content.replace("babase.Actor", "bascenev1.Actor")
    content = content.replace("babase.Player", "bascenev1.Player")
    content = content.replace("babase.PlayerDiedMessage", "bascenev1.PlayerDiedMessage")
    content = content.replace("babase.time", "bascenev1.time")
    content = content.replace("babase.Timer", "bascenev1.Timer")
    content = content.replace("babase.newnode", "bascenev1.newnode")
    content = content.replace("babase.Node", "bascenev1.Node")
    content = content.replace("babase.emitfx", "bascenev1.emitfx")
    content = content.replace("babase.animate", "bascenev1.animate")
    content = content.replace("babase.FreeForAllSession", "bascenev1.FreeForAllSession")
    content = content.replace("babase.DualTeamSession", "bascenev1.DualTeamSession")
    content = content.replace("babase.MultiTeamSession", "bascenev1.MultiTeamSession")
    content = content.replace("babase.EndSession", "bascenev1.EndSession")
    content = content.replace("babase.CoopSession", "bascenev1.CoopSession")
    content = content.replace("babase.TeamGameActivity", "bascenev1.TeamGameActivity")
    content = content.replace("babase.Team", "bascenev1.Team")
    content = content.replace("babase.Session", "bascenev1.Session")
    content = content.replace("babase.getsession", "bascenev1.getsession")
    content = content.replace("babase.Material", "bascenev1.Material")
    content = content.replace("babase.WeakCall", "bascenev1.WeakCall")
    content = content.replace("babase.DieMessage", "bascenev1.DieMessage")
    content = content.replace("babase.OutOfBoundsMessage", "bascenev1.OutOfBoundsMessage")
    content = content.replace("babase.DroppedMessage", "bascenev1.DroppedMessage")
    content = content.replace("babase.HitMessage", "bascenev1.HitMessage")
    content = content.replace("babase.ThawMessage", "bascenev1.ThawMessage")
    content = content.replace("babase.NotFoundError", "bascenev1.NotFoundError")
    content = content.replace("babase.getcollision", "bascenev1.getcollision")
    content = content.replace("babase.app.lang", "bascenev1.app.lang")
    content = content.replace("babase.MusicType", "bascenev1.MusicType")
    content = content.replace("babase.getactivity", "bascenev1.getactivity")
    content = content.replace("babase.getactivity", "bascenev1.getactivity")
    content = content.replace("babase.CelebrateMessage", "bascenev1.CelebrateMessage")
    content = content.replace("babase.ScoreConfig", "bascenev1.ScoreConfig")
    content = content.replace("babase.ScoreType", "bascenev1.ScoreType")
    content = content.replace("babase.GameResults", "bascenev1.GameResults")
    content = content.replace("babase.getmaps", "bascenev1.app.classic.getmaps")
    content = content.replace("babase.cameraflash", "bascenev1.cameraflash")
    content = content.replace("babase.getmodel", "bascenev1.getmesh")
    content = content.replace("babase.Map", "bascenev1.Map")
    content = content.replace("babase.DeathType", "bascenev1.DeathType")
    content = content.replace("babase.GameActivity", "bascenev1.GameActivity")
    content = content.replace("_babase.app.stress_test_reset_timer", "_babase.app.classic.stress_test_reset_timer")
    content = content.replace("babase.app.stress_test_reset_timer", "_babase.app.classic.stress_test_reset_timer")
    content = content.replace("babase._map", "bascenev1._map")
    content = content.replace("babase._session.", "bascenev1._session.")
    content = content.replace("babase._activity", "bascenev1._activity")
    content = content.replace("_babase.get_client_public_device_uuid", "_bascenev1.get_client_public_device_uuid")
    content = content.replace("babase.PickedUpMessage", "bascenev1.PickedUpMessage")
    content = content.replace("babase.PowerupMessage", "bascenev1.PowerupMessage")
    content = content.replace("babase.FreezeMessage", "bascenev1.FreezeMessage")
    content = content.replace("with babase.ContextRef(activity):", "with activity.context:")
    content = content.replace("babase.Context", "babase.ContextRef")
    content = content.replace("babase._dualteamsession", "bascenev1._dualteamsession")
    content = content.replace("babase._freeforallsession", "bascenev1._freeforallsession")
    content = content.replace("babase._multiteamsession", "bascenev1._multiteamsession")
    content = content.replace("babase._gameactivity", "bascenev1._gameactivity")
    content = content.replace("babase._powerup", "bascenev1._powerup")
    content = content.replace("babase.Chooser", "bascenev1.Chooser")
    content = content.replace("babase._lobby", "bascenev1._lobby")
    content = content.replace("babase._stats", "bascenev1._stats")
    content = content.replace("babase._team", "bascenev1._team")
    content = content.replace("PlayerType", "PlayerT")
    content = content.replace("babase.app.spaz_appearances", "babase.app.classic.spaz_appearances")
    content = content.replace("babase._coopsession", "bascenev1._coopsession")
    content = content.replace("babase._servermode", "baclassic._servermode")
    content = content.replace("_babase.app.server", "babase.app.classic.server")
    content = content.replace("_babase.chatmessage", "bascenev1.chatmessage")
    content = content.replace("_babase.disconnect_client", "_bascenev1.disconnect_client")
    content = content.replace("_babase.get_game_roster", "bascenev1.get_game_roster")
    content = content.replace("_babase.get_public_party_max_size", "bascenev1.get_public_party_max_size")
    content = content.replace("_babase.new_host_session", "bascenev1.new_host_session")
    content = content.replace("babase._playlist", "bascenev1._playlist")
    content = content.replace("model", "mesh")
    content = content.replace("TimeType.REAL", "use `bascenev1.apptimer` in `activity.context` instead")
    content = content.replace("_babase.app.coop_session_args", "babase.app.classic.coop_session_args")
    content = content.replace("_babase.app.campaigns", "babase.app.classic.campaigns")

    content = content.replace("_babase.newactivity", "bascenev1.newactivity")
    content = content.replace("babase.Window", "bauiv1.Window")
    content = content.replace("babase.Widget", "bauiv1.Widget")
    content = content.replace("babase.widget", "bauiv1.widget")
    content = content.replace("babase.containerwidget", "bauiv1.containerwidget")
    content = content.replace("babase.scrollwidget", "bauiv1.scrollwidget")
    content = content.replace("babase.buttonwidget", "bauiv1.buttonwidget")
    content = content.replace("babase.textwidget", "bauiv1.textwidget")
    content = content.replace("babase.checkboxwidget", "bauiv1.checkboxwidget")
    content = content.replace("babase.imagewidget", "bauiv1.imagewidget")
    content = content.replace("babase.uicleanupcheck", "bauiv1.uicleanupcheck")
    content = content.replace("_babase.set_public_party_max_size", "bascenev1.set_public_party_max_size")
    content = content.replace("_bauiv1", "bauiv1")
    content = content.replace("babase.show_damage_count", "bascenev1.show_damage_count")
    content = content.replace("babase._gameutils", "bascenev1._gameutils")
    content = content.replace("babase.StandMessage", "bascenev1.StandMessage")
    content = content.replace("babase.PowerupAcceptMessage", "bascenev1.PowerupAcceptMessage")
    content = content.replace("babase._gameutils", "bascenev1._gameutils")
    content = content.replace("babase.camerashake", "bascenev1.camerashake")
    content = content.replace("babase.app.add_coop_practice_level", "babase.app.classic.add_coop_practice_level")
    content = content.replace("babase._campaign", "bascenev1._campaign")
    content = content.replace("babase.Level", "bascenev1._level.Level")
    content = content.replace("babase.app.cloud.send_message_cb", "bauiv1.app.plus.cloud.send_message_cb")
    content = content.replace("_babase.get_special_widget", "bauiv1.get_special_widget")

    content = content.replace(".app.platform", ".app.classic.platform")
    content = content.replace(".app.subplatform", ".app.classic.subplatform")
    content = content.replace(".getlog", ".get_v1_cloud_log")
    # Converting `ba.playsound(abc)` to `abc.play()` is tricky.
    # Do it manually in case regex substitution fails.# Do it manually in case regex substitution fails. Are you sure!!
    #! FIXME May cause syntax warning on 3.12 with this code below
    content = re.sub(r'babase\.playsound\(([^,\n]+)(,\s*([^,\n]+))?(,\s*position=([^,\n]+))?\)', r'\1.play(\3\5)', content, flags=re.MULTILINE)
    # content = re.sub(
    #     r'babase\.playsound\(\s*([^,\n]+),\s*([^,\n]+)\)',
    #     r'\1.play(\2)',
    #     content,
    #     flags=re.MULTILINE
    # )
    # content = re.sub(
    #     r'babase\.playsound\(\s*([^,\n]+),\s*([^,\n]+),\s*position=([^,\n]+)\)',
    #     r'\1.play(\2, position=\3)',
    #     content,
    #     flags=re.MULTILINE
    # )
    # content = re.sub("babase\.playsound\((.+?), (.+?), (.+?)\)", "\\1.play(\\2, \\3)", content)
    # content = re.sub(
    #     r'babase\.playsound\(([^,\n]+),\s*position=([^,\n]+)\)',
    #     r'\1.play(position=\2)',
    #     content
    # )
    # content = re.sub("babase\.playsound\((.*)\)", "\\1.play()", content)

    # Removed in API 8:
    # content = content.replace("babase.internal.set_telnet_access_enabled", "")

    content = content.replace("babase.internal.add_transaction", "bauiv1.app.plus.add_v1_account_transaction")
    content = content.replace("babase.internal.run_transaction", "bauiv1.app.plus.run_v1_account_transaction")
    content = content.replace("_babase.add_transaction", "bauiv1.app.plus.add_v1_account_transaction")
    content = content.replace("_babase.run_transactions", "bauiv1.app.plus.run_v1_account_transactions")
    content = content.replace("babase._store.get_store_layout", "bauiv1.app.classic.store.get_store_layout")
    content = content.replace("babase.internal.get_store_layout", "bauiv1.app.classic.store.get_store_layout")
    content = content.replace("babase.internal.connect_to_party", "bascenev1.connect_to_party")
    content = content.replace("babase.internal.get_default_powerup_distribution", "bascenev1._powerup.get_default_powerup_distribution")
    content = content.replace("babase.internal.DEFAULT_REQUEST_TIMEOUT_SECONDS", "babase.DEFAULT_REQUEST_TIMEOUT_SECONDS")
    content = content.replace("babase.internal.DEFAULT_TEAM_COLORS", "bascenev1.DEFAULT_TEAM_COLORS")
    content = content.replace("babase.internal.DEFAULT_TEAM_NAMES", "bascenev1.DEFAULT_TEAM_NAMES")
    content = content.replace("babase.internal.JoinActivity", "bascenev1.JoinActivity")
    content = content.replace("babase.internal.LoginAdapter", "babase._login.LoginAdapter")
    content = content.replace("babase.internal.PlayerProfilesChangedMessage", "bascenev1._messages.PlayerProfilesChangedMessage")
    content = content.replace("babase.internal.ScoreScreenActivity", "bascenev1.ScoreScreenActivity")
    content = content.replace("babase.internal.add_clean_frame_callback", "babase.add_clean_frame_callback")
    content = content.replace("babase.internal.android_get_external_files_dir", "babase.android_get_external_files_dir")
    content = content.replace("babase.internal.appname", "babase.appname")
    content = content.replace("babase.internal.appnameupper", "babase.appnameupper")
    content = content.replace("babase.internal.capture_gamepad_input", "bascenev1.capture_gamepad_input")
    content = content.replace("babase.internal.capture_keyboard_input", "bascenev1.capture_keyboard_input")
    content = content.replace("babase.internal.charstr", "babase.charstr")
    content = content.replace("babase.internal.chatmessage", "bascenev1.chatmessage")
    content = content.replace("babase.internal.commit_app_config", "bauiv1.commit_app_config")
    content = content.replace("babase.internal.disconnect_client", "bascenev1.disconnect_client")
    content = content.replace("babase.internal.disconnect_from_host", "bascenev1.disconnect_from_host")
    content = content.replace("babase.internal.do_play_music", "babase.app.classic.music.do_play_music")
    content = content.replace("babase.internal.end_host_scanning", "bascenev1.end_host_scanning")
    content = content.replace("babase.internal.fade_screen", "bauiv1.fade_screen")
    content = content.replace("babase.internal.filter_playlist", "bascenev1.filter_playlist")
    content = content.replace("babase.internal.game_service_has_leaderboard", "_baplus.game_service_has_leaderboard")
    content = content.replace("babase.internal.get_available_purchase_count", "bauiv1.app.classic.store.get_available_purchase_count")
    content = content.replace("babase.internal.get_available_sale_time", "bauiv1.app.classic.store.get_available_sale_time")
    content = content.replace("babase.internal.get_chat_messages", "bascenev1.get_chat_messages")
    content = content.replace("babase.internal.get_clean_price", "bauiv1.app.classic.store.get_clean_price")
    content = content.replace("babase.internal.get_connection_to_host_info", "bascenev1.get_connection_to_host_info")
    content = content.replace("babase.internal.get_default_free_for_all_playlist", "bascenev1._playlist.get_default_free_for_all_playlist")
    content = content.replace("babase.internal.get_default_teams_playlist", "bascenev1._playlist.get_default_teams_playlist")
    content = content.replace("babase.internal.get_display_resolution", "babase.get_display_resolution")
    content = content.replace("babase.internal.get_filtered_map_name", "bascenev1._map.get_filtered_map_name")
    content = content.replace("babase.internal.get_foreground_host_session", "bascenev1.get_foreground_host_session")
    content = content.replace("babase.internal.get_game_port", "bascenev1.get_game_port")
    content = content.replace("babase.internal.get_game_roster", "bascenev1.get_game_roster")
    content = content.replace("babase.internal.get_input_device_config", "bauiv1.app.classic.get_input_device_config")
    content = content.replace("babase.internal.get_ip_address_type", "babase.get_ip_address_type")
    content = content.replace("babase.internal.get_local_active_input_devices_count", "bascenev1.get_local_active_input_devices_count")
    content = content.replace("babase.internal.get_low_level_config_value", "bauiv1.get_low_level_config_value")
    content = content.replace("babase.internal.get_map_class", "bascenev1.get_map_class")
    content = content.replace("babase.internal.get_map_display_string", "bascenev1.get_map_display_string")
    content = content.replace("babase.internal.get_master_server_address", "bauiv1.app.plus.get_master_server_address")
    content = content.replace("babase.internal.get_max_graphics_quality", "babase.get_max_graphics_quality")
    content = content.replace("babase.internal.get_news_show", "_babase.app.plus.get_news_show")
    content = content.replace("babase.internal.get_next_tip", "bascenev1.app.classic.get_next_tip") 
    content = content.replace("babase.internal.get_player_colors", "bascenev1.get_player_colors")
    content = content.replace("babase.internal.get_player_profile_colors", "bascenev1.get_player_profile_colors")
    content = content.replace("babase.internal.get_player_profile_icon", "bascenev1.get_player_profile_icon")
    content = content.replace("babase.internal.get_price", "bauiv1.app.plus.get_price")
    content = content.replace("babase.internal.get_public_party_enabled", "bascenev1.get_public_party_enabled")
    content = content.replace("babase.internal.get_public_party_max_size", "bascenev1.get_public_party_max_size")
    content = content.replace("babase.internal.get_purchased", "bauiv1.app.plus.get_purchased")
    content = content.replace("babase.internal.get_purchases_state", "_baplus.get_purchases_state")
    content = content.replace("babase.internal.get_qrcode_texture", "bauiv1.get_qrcode_texture")
    content = content.replace("babase.internal.get_random_names", "bascenev1.get_random_names")
    content = content.replace("babase.internal.get_remote_app_name", "bascenev1.get_remote_app_name")
    content = content.replace("babase.internal.get_replay_speed_exponent", "bascenev1.get_replay_speed_exponent")
    content = content.replace("babase.internal.get_replays_dir", "babase.get_replays_dir")
    content = content.replace("babase.internal.get_special_widget", "bauiv1.get_special_widget")
    content = content.replace("babase.internal.get_store_item", "babase.app.classic.store.get_store_item")
    content = content.replace("babase.internal.get_store_item_display_size", "babase.app.classic.store.get_store_item_display_size")
    content = content.replace("babase.internal.get_store_item_name_translated", "babase.app.classic.store.get_store_item_name_translated")
    content = content.replace("babase.internal.get_string_height", "babase.get_string_height")
    content = content.replace("babase.internal.get_string_width", "babase.get_string_width")
    content = content.replace("babase.internal.get_tournament_prize_strings", "bascenev1.app.classic.get_tournament_prize_strings")
    content = content.replace("babase.internal.get_trophy_string", "bascenev1.get_trophy_string")
    content = content.replace("babase.internal.get_type_name", "babase.get_type_name")
    content = content.replace("babase.internal.get_ui_input_device", "bascenev1.get_ui_input_device")
    content = content.replace("babase.internal.get_unowned_game_types", "babase.app.classic.store.get_unowned_game_types")
    content = content.replace("babase.internal.get_unowned_maps", "babase.app.classic.store.get_unowned_maps")
    content = content.replace("babase.internal.get_v1_account_display_string", "bauiv1.app.plus.get_v1_account_display_string")
    content = content.replace("babase.internal.get_v1_account_misc_read_val", "bauiv1.app.plus.get_v1_account_misc_read_val")
    content = content.replace("babase.internal.get_v1_account_misc_read_val_2", "bauiv1.app.plus.get_v1_account_misc_read_val_2")
    content = content.replace("babase.internal.get_v1_account_misc_val", "bauiv1.app.plus.get_v1_account_misc_val")
    content = content.replace("babase.internal.get_v1_account_name", "bauiv1.app.plus.get_v1_account_name")
    content = content.replace("babase.internal.get_v1_account_state", "bauiv1.app.plus.get_v1_account_state")
    content = content.replace("babase.internal.get_v1_account_state_num", "bauiv1.app.plus.get_v1_account_state_num")
    content = content.replace("babase.internal.get_v1_account_ticket_count", "bauiv1.app.plus.get_v1_account_ticket_count")
    content = content.replace("babase.internal.get_v1_account_type", "bauiv1.app.plus.get_v1_account_type")
    content = content.replace("babase.internal.get_v2_fleet", "_baplus.get_v2_fleet")
    content = content.replace("babase.internal.getcampaign", "bauiv1.app.classic.getcampaign")
    content = content.replace("babase.internal.getclass", "babase.getclass")
    content = content.replace("babase.internal.getinputdevice", "bascenev1.getinputdevice")
    content = content.replace("babase.internal.has_gamma_control", "babase.has_gamma_control")
    content = content.replace("babase.internal.has_video_ads", "bauiv1.has_video_ads")
    content = content.replace("babase.internal.have_incentivized_ad", "bauiv1.have_incentivized_ad")
    content = content.replace("babase.internal.have_permission", "babase.have_permission")
    content = content.replace("babase.internal.have_touchscreen_input", "bascenev1.have_touchscreen_input")
    content = content.replace("babase.internal.host_scan_cycle", "bascenev1.host_scan_cycle")
    content = content.replace("babase.internal.in_game_purchase", "bui.app.plus.in_game_purchase")
    content = content.replace("babase.internal.increment_analytics_count", "babase.increment_analytics_count")
    content = content.replace("babase.internal.is_blessed", "bui.app.plus.is_blessed")
    content = content.replace("babase.UISubsystem","bauiv1.UIV1AppSubsystem")
    content = content.replace("babase.internal.is_browser_likely_available", "bauiv1.is_browser_likely_available")
    content = content.replace("babase.internal.is_in_replay", "bascenev1.is_in_replay")
    content = content.replace("babase.internal.is_party_icon_visible", "bauiv1.is_party_icon_visible")
    content = content.replace("babase.internal.is_running_on_fire_tv", "babase.is_running_on_fire_tv")
    content = content.replace("babase.internal.is_xcode_build", "babase.is_xcode_build")
    content = content.replace("babase.internal.json_prep", "babase.json_prep")
    content = content.replace("babase.internal.lock_all_input", "babase.lock_all_input")
    content = content.replace("babase.internal.mark_config_dirty", "_babase.app.plus.mark_config_dirty")
    content = content.replace("babase.internal.new_host_session", "bascenev1.new_host_session")
    content = content.replace("babase.internal.new_replay_session", "bascenev1.new_replay_session")
    content = content.replace("babase.internal.open_file_externally", "bauiv1.open_file_externally")
    content = content.replace("babase.internal.power_ranking_query", "_baplus.power_ranking_query")
    content = content.replace("babase.internal.preload_map_preview_media", "bauiv1.app.classic.preload_map_preview_media")
    content = content.replace("babase.internal.purchase", "_baplus.purchase")
    content = content.replace("babase.internal.register_map", "bascenev1.register_map")
    content = content.replace("babase.internal.release_gamepad_input", "bascenev1.release_gamepad_input")
    content = content.replace("babase.internal.release_keyboard_input", "bascenev1.release_keyboard_input")
    content = content.replace("babase.internal.report_achievement", "babase.app.plus.report_achievement")
    content = content.replace("babase.internal.request_permission", "babase.request_permission")
    content = content.replace("babase.internal.reset_achievements", "_baplus.reset_achievements")
    content = content.replace("babase.internal.reset_random_player_names", "bascenev1.reset_random_player_names")
    content = content.replace("babase.internal.restore_purchases", "_baplus.restore_purchases")
    content = content.replace("babase.internal.run_cpu_benchmark", "baclassic._benchmark.run_cpu_benchmark")
    content = content.replace("babase.internal.run_gpu_benchmark", "baclassic._benchmark.run_gpu_benchmark")
    content = content.replace("babase.internal.run_media_reload_benchmark", "baclassic._benchmark.run_media_reload_benchmark")
    content = content.replace("babase.internal.run_stress_test", "babase.app.classic.run_stress_test")
    content = content.replace("babase.internal.set_authenticate_clients", "bascenev1.set_authenticate_clients")
    content = content.replace("babase.internal.set_debug_speed_exponent", "bascenev1.set_debug_speed_exponent")
    content = content.replace("babase.internal.set_low_level_config_value", "babase.set_low_level_config_value")
    content = content.replace("babase.internal.set_party_icon_always_visible", "bauiv1.set_party_icon_always_visible")
    content = content.replace("babase.internal.set_party_window_open", "bauiv1.set_party_window_open")
    content = content.replace("babase.internal.set_public_party_enabled", "bascenev1.set_public_party_enabled")
    content = content.replace("babase.internal.set_public_party_max_size", "bascenev1.set_public_party_max_size")
    content = content.replace("babase.internal.set_public_party_name", "bascenev1.set_public_party_name")
    content = content.replace("babase.internal.set_public_party_queue_enabled", "bascenev1.set_public_party_queue_enabled")
    content = content.replace("babase.internal.set_replay_speed_exponent", "bascenev1.set_replay_speed_exponent")
    content = content.replace("babase.internal.set_touchscreen_editing", "bascenev1.set_touchscreen_editing")
    content = content.replace("babase.internal.set_ui_input_device", "babase.set_ui_input_device")
    content = content.replace("babase.internal.should_submit_debug_info", "babase._apputils.should_submit_debug_info")
    content = content.replace("babase.internal.show_online_score_ui", "bauiv1.show_online_score_ui")
    content = content.replace("babase.internal.sign_in_v1", "babase.app.plus.sign_in_v1")
    content = content.replace("babase.internal.sign_out_v1", "babase.app.plus.sign_out_v1")
    content = content.replace("babase.internal.submit_score", "bascenev1.app.plus.submit_score")
    content = content.replace("babase.internal.tournament_query", "_baplus.tournament_query")
    content = content.replace("babase.internal.unlock_all_input", "babase.unlock_all_input")
    content = content.replace("babase.internal.value_test", "bauiv1.app.classic.value_test")
    content = content.replace("babase.internal.workspaces_in_use", "babase.workspaces_in_use")
    content = content.replace("babase.internal.dump_tracebacks", "babase._apputils.dump_app_state")
    content = content.replace("babase.internal.show_app_invite", "_bauiv1.show_app_invite")
    content = content.replace("babase.internal.master_server_get", "babase.app.classic.master_server_v1_get")
    content = content.replace("babase.internal.master_server_post", "babase.app.classic.master_server_v1_post")
    content = content.replace("babase.internal.log_dumped_tracebacks", "babase._apputils.log_dumped_app_state")
    content = content.replace("babase.internal.have_outstanding_transactions", "bauiv1.app.plus.have_outstanding_v1_account_transactions")
    content = content.replace("babase.internal.get_public_login_id", "bauiv1.app.plus.get_v1_account_public_login_id")
    content = content.replace("babase.internal.get_input_map_hash", "bauiv1.app.classic.get_input_device_map_hash")
    content = content.replace("babase.internal.get_device_value", "bauiv1.app.classic.get_input_device_mapped_value")
    content = content.replace("babase.internal.", "bascenev1")
    # content = content.replace("babase.internal", "")

    content = content.replace("babase._generated", "babase._mgen")
    content = content.replace("_babase.disconnect_from_host", "bascenev1.disconnect_from_host")
    content = content.replace("babase.disconnect_from_host", "bascenev1.disconnect_from_host")
    content = content.replace("_babase.connect_to_party", "bascenev1.connect_to_party")
    content = content.replace("babase.connect_to_party", "bascenev1.connect_to_party")
    content = content.replace("babase.set_party_window_open", "bauiv1.set_party_window_open")
    content = content.replace("babase.set_party_window_open", "bauiv1.set_party_window_open")
    content = content.replace("babase.getcollidemesh", "bascenev1.getcollisionmesh")
    content = content.replace("collide_mesh", "collision_mesh")
    content = content.replace("babase.FloatSetting", "bascenev1.FloatSetting")
    content = content.replace("babase.playsound", "bascenev1.playsound")
    content = content.replace("bascenev1.time(timeformat=babase.TimeFormat.MILLISECONDS)", "bascenev1.time() * 1000")
    
    content = content.replace("babase.app.build_number", "babase.app.env.engine_build_number")
    content = content.replace("babase.app.device_name", "babase.app.env.device_name")
    content = content.replace("babase.app.config_file_path", "babase.app.env.config_file_path")
    content = content.replace("babase.app.version", "babase.app.env.engine_version")
    content = content.replace("babase.app.debug_build", "babase.app.env.debug")
    content = content.replace("babase.app.test_build", "babase.app.env.test")
    content = content.replace("babase.app.data_directory", "babase.app.env.data_directory")
    content = content.replace("babase.app.python_directory_user", "babase.app.env.python_directory_user")
    content = content.replace("babase.app.python_directory_app", "babase.app.env.python_directory_app")
    content = content.replace("babase.app.python_directory_app_site", "babase.app.env.python_directory_app_site")
    content = content.replace("babase.app.api_version", "babase.app.env.api_version")
    content = content.replace("babase.app.on_tv", "babase.app.env.tv")
    content = content.replace("babase.app.vr_mode", "babase.app.env.vr")
    content = content.replace("babase.app.toolbar_test", "_bauiv1.toolbar_test")
    content = content.replace("babase.app.arcade_mode", "babase.app.env.arcade")
    content = content.replace("babase.app.headless_mode", "babase.app.env.headless")
    content = content.replace("babase.app.demo_mode", "babase.app.env.demo")
    content = content.replace("babase.app.protocol_version", "bascenev1.protocol_version")
    content = content.replace("bascenev1.get_connection_to_host_info", "bascenev1.get_connection_to_host_info_2")

    content = content.replace("babase._store", "bauiv1.app.classic.store")
    content = content.replace("bastd.ui", "bauiv1lib")
    content = content.replace("bastd", "bascenev1lib")
    content = content.replace("timetype=","")
    content = content.replace("babase.columnwidget", "bauiv1.columnwidget")
    content = content.replace("_babase.get_game_port", "bascenev1.get_game_port")
    content = content.replace("_babase.get_chat_messages", "bascenev1.get_chat_messages")
    content = content.replace("_babase.get_foreground_host_session", "bascenev1.get_foreground_host_session")
    content = content.replace("_babase.get_foreground_host_activity", "bascenev1.get_foreground_host_activity")
    content = content.replace("bascenev1.SessionPlayerNotFoundError", "babase.SessionPlayerNotFoundError")
    content = content.replace("bascenev1", "bs")
    content = content.replace("bauiv1", "bui")
    content = content.replace("import bs", "import bascenev1 as bs")
    content = content.replace("import bui", "import bauiv1 as bui")
    content = content.replace("bslib", "bascenev1lib")
    content = content.replace("builib", "bauiv1lib")
    content = content.replace("from bs.", "from bascenev1.")
    content = content.replace("from bui.", "from bauiv1.")
    content = content.replace("import bascenev1 as bascenev1lib", "import bascenev1lib")
    content = content.replace("import bauiv1 as bauiv1lib", "import bauiv1lib")
    content = content.replace("# ba_meta export bs.GameActivity", "# ba_meta export bascenev1.GameActivity")
    content = content.replace("_bs", "bs")

    content = re.sub(r'bs\.Timer\(([^)]*)\bTimeType\.REAL\b([^)]*)\)', r'babase.AppTimer(\1\2)', content)
    
    return content

def api8_to_api9(content:str) -> str:
    content = content.replace("# ba_meta require api 8", "# ba_meta require api 9")
    content = content.replace("# ba_meta export plugin", "# ba_meta export babase.Plugin")
    content = content.replace("bs.get_connection_to_host_info", "get_connection_to_host_info_2")
    # replace get_connection_to_host_info_2(args)["name"] with et_connection_to_host_info_2(args).name
    content = re.sub(r"bs\.get_connection_to_host_info_2\((.*?)\)\\[\"name\"]", r"bs.get_connection_to_host_info_2(\1).name", content)
    content = content.replace("bauiv1.Window", "bauiv1.MainWindow")
    # To find and remove bauiv1.is_party_icon_visible(something) removed in api 9
    content = re.sub(r'bauiv1\.is_party_icon_visible\([^\)]*\)', '', content)
    content = content.replace("babase.env()[\"ui_scale\"]","babase.get_ui_scale()")
    
    return content


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Port plugins from api 6 to api 9",
        exit_on_error=False
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        type=str,
        help="File path of the plugin."
    )
    parser.add_argument(
        "-t", "--type",
        required=True,
        type=str,
        help="Type of plugin (client or server)."
    )
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as error:
        print(error)
        parser.print_help()
        exit(1)
    file_path = Path(args.file)
    plugin_type= args.type

    if not file_path.exists():
        print(f"Error: The file '{file_path}' does not exist.")
        exit(1)

    if encoding:=detect_file_encoding(file_path): # behold the walrus operator XDD
        with open(file_path, 'r', encoding=encoding) as read_f:
            print("Porting "+ file_path.name)
            file_text = read_f.read()
            file_text = api6_to_api8(file_text,plugin_type=plugin_type)
            file_text = api8_to_api9(file_text)
            with open(file_path, 'w', encoding=encoding) as write_f:
                write_f.write(TRADEMARK + file_text)
    else:
        print('Could not detect encoding')

if __name__ == "__main__":
    main()

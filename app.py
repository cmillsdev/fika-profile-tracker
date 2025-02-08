from flask import Flask, render_template, request, session, redirect, url_for
from utils.helpers import id_lookup, load_json, get_all_players, get_profile
from core.quests import get_all_objectives
from core.hideout import get_all_hideout
from core.stats import get_all_stats
from core.overview import get_overview
from core.alerts import get_alerts
from core.version import get_version
app = Flask(__name__)
#my_profile = Profile(load_json('profiles/674e8d5e000124d3a4adc638.json'))

#print(get_objectives('59674cd986f7744ab26e32f2', my_profile.profile_id))

#print(quests.get_all_objectives(my_profile.profile_id))

app.secret_key = 'your_secret_key_here'  # Required for sessions

@app.route("/")
def player_selection():
    players = get_all_players()
    return render_template("players.html", players=players)

@app.route("/select_player", methods=["POST"])
def select_player():
    player_id = request.form.get("player_id")
    session['player_id'] = player_id  # Store player_id in session
    session['profile'] = get_profile(player_id)
    return redirect(url_for("overview", pid=player_id))
    
@app.route("/overview/<pid>")
def overview(pid):
    if 'player_id' not in session or session['player_id'] != pid:
        return redirect(url_for("player_selection"))  # Redirect if player_id is not in session
    profile = session.get('profile') or get_profile(pid)
    overview = get_overview(pid)
    alerts = get_alerts(pid)
    players = get_all_players()  # Fetch players
    version = get_version(pid)
    return render_template("overview.html", overview=overview, alerts=alerts, player_id=pid, players=players, version=version)

@app.route("/quests/<pid>")
def quests(pid):
    if 'player_id' not in session or session['player_id'] != pid:
        return redirect(url_for("player_selection"))  # Redirect if player_id is not in session
    profile = session.get('profile') or get_profile(pid)
    quests = get_all_objectives(pid, profile['Quests'])
    players = get_all_players()  # Fetch players
    version = get_version(pid)
    return render_template("quests.html", quests=quests, player_id=pid, players=players, version=version)

@app.route("/stats/<pid>")
def stats(pid):
    if 'player_id' not in session or session['player_id'] != pid:
        return redirect(url_for("player_selection"))  # Redirect if player_id is not in session
    profile = session.get('profile') or get_profile(pid)
    stats = get_all_stats(pid, profile)
    players = get_all_players()  # Fetch players
    version = get_version(pid)
    return render_template("stats.html", stats=stats, player_id=pid, players=players, version=version)

@app.route("/hideout/<pid>")
def hideout(pid):
    if 'player_id' not in session or session['player_id'] != pid:
        return redirect(url_for("player_selection"))  # Redirect if player_id is not in session
    profile = session.get('profile') or get_profile(pid)
    hideout = get_all_hideout(pid, profile['Hideout'])
    players = get_all_players()  # Fetch players
    version = get_version(pid)
    return render_template("hideout.html", hideout=hideout, player_id=pid, players=players, version=version)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
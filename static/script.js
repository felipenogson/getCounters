const searchChamp = document.getElementById('champion');
const suggestions = document.getElementById('suggestions');
const resultsEl = document.getElementById('results');

// Getting champions from json
champions = []
// fetch('../static/champions.json')
fetch('https://raw.githubusercontent.com/ngryman/lol-champions/master/champions.json')
    .then(req => req.json())
    .then(data => {
        champions.push(...data);
        if(document.getElementById('results')){
            showIconResults();
        }
    });

// Filter the champions from a word
function findMatches(word, champions) {
    return champions.filter(champ => {
        const regex = new RegExp(word, 'gi');
        return champ.name.match(regex);
    });
}

// push matches into DOM
function displayMatches() {
    const matchArr = findMatches(this.value, champions);
    const html = matchArr.map(champ => {
        const regex = new RegExp(this.value, 'gi');
        const champName = champ.name.replace(regex, `<span class="hl">${this.value}</span>`)
        return `<li><img src="${champ.icon}" class="champ"><span class="name">${champName}</span></li>`
    }).join('');
    suggestions.innerHTML = html;
    if (searchChamp.value == '') {
        suggestions.innerHTML = '';
    }
}

// Select a hero from the list
function selectHero(e) {
    console.log(e.target.textContent);
    searchChamp.value = e.target.textContent;
    suggestions.innerHTML = '';
}

// Put icons in the results tables
function showIconResults(){
    champList = [...document.getElementsByClassName('champ-list')];
    champList.forEach( td => { 
        champ = champions.filter( el => el.id == td.textContent.replace(/\s/g,''))[0]; 
        console.log(champ);
        td.innerHTML = `<td class="champ-list"><a href="https://www.leagueofgraphs.com/champions/builds/${champ.id}" target="_new_window"><img class="champ" src="${champ.icon}">${champ.name}<a></td>`;
    })
}

searchChamp.addEventListener('keyup', displayMatches);
suggestions.addEventListener('click', selectHero);


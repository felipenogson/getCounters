const searchChamp = document.getElementById('champion');
const suggestions = document.getElementById('suggestions');

// Getting champions from json
champions =  []
// fetch('../static/champions.json')
fetch('https://raw.githubusercontent.com/ngryman/lol-champions/master/champions.json')
    .then( req => req.json())
    .then( data => {
        champions.push(...data);
    });

// Filter the champions from a word
function findMatches(word, champions){
    return champions.filter( champ => {
        const regex = new RegExp(word, 'gi');
        return champ.name.match(regex);
    });
}

// push matches into DOM
function displayMatches(){
    const matchArr = findMatches(this.value, champions);
    const html = matchArr.map( champ => {
        const regex = new RegExp(this.value, 'gi');
        const champName = champ.name.replace(regex, `<span class="hl">${this.value}</span>`)
        return `<li><img src="${champ.icon}" class="champ"><span class="name">${champName}</span></li>`
    }).join('');
    suggestions.innerHTML = html;
    if(searchChamp.value == '' ){
        suggestions.innerHTML = '' ;
    }
}

// Select a hero from the list
function selectHero(e){
    console.log(e.target.textContent);
    searchChamp.value = e.target.textContent;
    suggestions.innerHTML = '';
}

searchChamp.addEventListener('keyup', displayMatches);
suggestions.addEventListener('click', selectHero);
const shortenStroke = (stroke) => {
    if (stroke.includes("Freestyle")) {
        return "Free";
    } else if (stroke.includes("Breaststroke")) {
        return "Breast";
    } else if (stroke.includes("Backstroke")) {
        return "Back";
    } else if (stroke.includes("Butterfly")) {
        return "Fly"
    } else if (stroke.includes("Medley")) {
        return "Med"
    } else {
        return stroke;
    }
}

const getUnitText = (unit) => {
    if (unit === "meters") {
        return "m";
    } else if (unit === "yards") {
        return "yd";
    } else {
        return unit;
    }
}

const getSexText = (sex, age) => {
    if (sex != "male" && sex != "female") {
        return sex;
    }
    if (age < 18) {
        return (sex == "male") ? "boys" : "girls";
    } else {
        return (sex == "male") ? "mens" : "womens";
    }
}

const getStrokeText = (stroke, relay, shortenName) => {
    if (relay == "individual" && stroke == "medley") return "IM";

    let strokeString = "";
    if (shortenName) {
        strokeString += shortenStroke(stroke)
    } else {
        strokeString += stroke;
    }
    if (relay === "relay") {
        strokeString += " relay";
    }
    return strokeString;
}

export const getStrokeCombinedText = (includeSex, includeAge, shortenName, includeDistance, start) => {
    let heats = start.heats;
    if (!heats || heats.length == 0) return "No heats";
    var ages = [];
    var sexesByAge = {};

    heats.forEach(function(heat) {
        const event = heat.event
        const ageGroup = event.min_age + "-" + event.max_age
        if (!ages.includes(ageGroup)) {
            ages.push(ageGroup);
            sexesByAge[ageGroup] = new Set();
        }
        sexesByAge[ageGroup].add(getSexText(event.sex, event.max_age));
    });
    
    let buildingString = "";
    
    ages.forEach(function(age, index) {
        if (index !== 0) buildingString += "& ";
        if (includeSex) {
            const sexesByAgeArray = Array.from(sexesByAge[age]);
            for (let x = 0; x < sexesByAgeArray.length; x++) if (x !== 0) buildingString += ("& " + sexesByAgeArray[x] + " ");
        }
        if (includeAge) buildingString += age + " ";
    });

    if (includeDistance) buildingString += + heats[0].event.distance + getUnitText(heats[0].event.unit) + " ";

    buildingString += getStrokeText(heats[0].event.stroke, heats[0].event.relay, shortenName)
    return buildingString;
}
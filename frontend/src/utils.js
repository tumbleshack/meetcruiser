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

export const startDescriptionText = (start, includeSex = true, includeAge = true, shortenName = true, includeDistance = true) => {
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
            for (let x = 0; x < sexesByAgeArray.length; x++) {
                buildingString += sexesByAgeArray[x] + " ";
                if (x !== 0) buildingString += "& ";
            }
        }
        if (includeAge) buildingString += age + " ";
    });

    if (includeDistance) buildingString += + heats[0].event.distance + getUnitText(heats[0].event.unit) + " ";

    buildingString += getStrokeText(heats[0].event.stroke, heats[0].event.relay, shortenName)
    return buildingString;
}

export function joinArray(array, separator) {
    return array.reduce((p, c, idx) => {
        if (idx === 0)
            return [c];
        else
            return [...p, separator, c];
    }, []);
}

export const startNumberText = (start) => {
    var heats = start.heats;
    if (!heats || heats.length == 0) return "No heats";
    heats.sort((a,b) => a.event.number + a.number / 100000 - b.event.number + b.number / 100000);
    let eventNumbers = heats.map((heat) => heat.event.number);
    let heatNumbers = heats.map((heat) => heat.number)
    var text = []
    for (let x = 0; x < heats.length; x++) {
        text.push(<>{String(eventNumbers[x])}<sup>{String(heatNumbers[x])}</sup></>)
    }
    let returnVal = joinArray(text, <>&nbsp;&&nbsp;</>)
    return <>{returnVal}</>
}

export const bound = (min, max, val) => {
    return Math.max(Math.min(val, max), min);
}
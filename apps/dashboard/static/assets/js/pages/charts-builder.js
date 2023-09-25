
    // 
    var dayEntriesData = JSON.parse(document.getElementById("click-dynamic").textContent);

    var currentDate = new Date();
    var monthEntries = 0;
    var weekEntries = 0;
    var dayEntries = 0;

    for (var i = 0; i < dayEntriesData.length; i++) {
        var entryDate = new Date(dayEntriesData[i].tr_date);
        var timeDiff = Math.abs(currentDate - entryDate);
        var daysDiff = Math.floor(timeDiff / (1000 * 3600 * 24));

        if (daysDiff <= 30) {
            monthEntries += dayEntriesData[i].entries;
        }
        if (daysDiff <= 7) {
            weekEntries += dayEntriesData[i].entries;
        }
        if (daysDiff >= 0 && daysDiff <= 1) {
            dayEntries += dayEntriesData[i].entries;
        }
    }

    var dayEntriesContainer = document.getElementById("day-entries-container");
    var weekEntriesContainer = document.getElementById("week-entries-container");
    var monthEntriesContainer = document.getElementById("month-entries-container");
    dayEntriesContainer.textContent = dayEntries;
    weekEntriesContainer.textContent = weekEntries;
    monthEntriesContainer.textContent = monthEntries;
    // End 


    // Find result for 'The most popular souce' block
    function findMostDeviceEntries(deviceData) {
        let device = null;
        let entries = -Infinity;

        for (let i = 0; i < deviceData.length; i++) {
            let dict = deviceData[i];
            if (dict.entries > entries) {
                entries = dict.entries;
                device = dict.device;
            }
        }
        return device;
    }
    var linksData = JSON.parse(document.getElementById("device-types").textContent);
    var maxLinkContainer = document.getElementById("max-device-container");
    maxLinkContainer.textContent = findMostDeviceEntries(linksData);
    // End


    // Find result for 'The most popular souce' block
    function findMostLinkEntries(linksData) {
        let link = null;
        let entries = -Infinity;

        for (let i = 0; i < linksData.length; i++) {
            let dict = linksData[i];
            if (dict.entries > entries) {
                entries = dict.entries;
                link = dict.ref_link;
            }
        }
        return link;
    }
    var linksData = JSON.parse(document.getElementById("sources").textContent);
    var maxLinkContainer = document.getElementById("max-link-container");
    maxLinkContainer.textContent = findMostLinkEntries(linksData);
    // End


    // Create 'click dynamic' chart
    var clickDynamic = JSON.parse(document.getElementById('click-dynamic').textContent);
    var clickDynamicLabels = [];
    var clickDynamicEntries = [];

    for (var i = 0; i < clickDynamic.length; i++) {
        var dict = clickDynamic[i];
        var labels = dict["tr_date"].slice(0, 10);
        var entries = dict["entries"];

        clickDynamicLabels.push(labels);
        clickDynamicEntries.push(entries);
    }
    const ctx = document.getElementById('myChart');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: clickDynamicLabels,
            datasets: [{
                data: clickDynamicEntries,
                fill: true,
                borderColor: 'rgb(102, 193, 253)',
                backgroundColor: 'rgba(154, 202, 235, 0.3)',
                tension: 0.3,
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            }
        },
    });
    //  End 'click dynamic' chart


    // Create 'device types' chart
    var deviceTypes = JSON.parse(document.getElementById('device-types').textContent);
    var deviceTypesLabels = [];
    var deviceTypesEntries = [];

    for (var i = 0; i < deviceTypes.length; i++) {
        var dict = deviceTypes[i];
        var labels = dict["device"];
        var entries = dict["entries"];

        deviceTypesLabels.push(labels);
        deviceTypesEntries.push(entries);
    }
    const ctx1 = document.getElementById('myChart1');
    new Chart(ctx1, {
        type: 'polarArea',
        data: {
            labels: deviceTypesLabels,
            datasets: [{
                data: deviceTypesEntries,
            }]
        },
    });
    // End 'device types' chart


    // Create 'os-types' chart
    var osTypes = JSON.parse(document.getElementById('os-types').textContent);
    var osTypesLabels = [];
    var osTypesEntries = [];

    for (var i = 0; i < osTypes.length; i++) {
        var dict = osTypes[i];
        var labels = dict["os"];
        var entries = dict["entries"];

        osTypesLabels.push(labels);
        osTypesEntries.push(entries);
    }
    const ctx2 = document.getElementById('myChart2');
    new Chart(ctx2, {
        type: 'polarArea',
        data: {
            labels: osTypesLabels,
            datasets: [{
                data: osTypesEntries,
            }],
        },
    });
    // End 'os-types' chart


    // Create 'browser-types' chart
    var browserTypes = JSON.parse(document.getElementById('browser-types').textContent);
    var browserTypesLabels = [];
    var browserTypesEntries = [];

    for (var i = 0; i < browserTypes.length; i++) {
        var dict = browserTypes[i];
        var labels = dict["browser"];
        var entries = dict["entries"];

        browserTypesLabels.push(labels);
        browserTypesEntries.push(entries);
    }
    const ctx3 = document.getElementById('myChart3');
    new Chart(ctx3, {
        type: 'polarArea',
        data: {
            labels: browserTypesLabels,
            datasets: [{
                data: browserTypesEntries,
            }],
        },
    });
    // End 'browser-types' chart


    // Create 'sources' chart
    var sourceTypes = JSON.parse(document.getElementById('sources').textContent);
    var sourceTypesLabels = [];
    var sourceTypesEntries = [];
    for (var i = 0; i < sourceTypes.length; i++) {
        var dict = sourceTypes[i];
        var labels = dict["ref_link"];
        var entries = dict["entries"];

        sourceTypesLabels.push(labels);
        sourceTypesEntries.push(entries);
    }
    const ctx4 = document.getElementById('myChart4');
    new Chart(ctx4, {
        type: 'polarArea',
        data: {
            labels: sourceTypesLabels,
            datasets: [{
                data: sourceTypesEntries,
            }],
        },
    });
    // End 'sources' chart


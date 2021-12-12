var autocomplete;
var base_country = 'PL';

google.maps.event.addDomListener(window, "load", initAutoComplete())

function initAutoComplete(){
   autocomplete = new google.maps.places.Autocomplete(
       document.getElementsByName('localization')[0],
       {
           fields: ["formatted_address", "geometry", "name"],
           types: ['address'],
           componentRestrictions: {'country': [base_country.toLowerCase()]},
       })

   autocomplete.addListener('place_changed', onPlaceChanged());
}


function onPlaceChanged (){

    var place = autocomplete.getPlace();
    var address = document.getElementsByName('localization')[0].value

    if (!place){
            document.getElementsByName('localization')[0].placeholder = "Wpisz adres";
    }
    else{

        for (var i = 0; i < place.address_components.length; i++) {
            for (var j = 0; j < place.address_components[i].types.length; j++) {

                if (place.address_components[i].types[j] == "street_number") {
                    var num = place.address_components[i].long_name;
                }
                if (place.address_components[i].types[j] == "route") {
                    var address = place.address_components[i].long_name;
                }
                if (place.address_components[i].types[j] == "postal_town") {
                     var town = place.address_components[i].long_name;
                }
                if (place.address_components[i].types[j] == "administrative_area_level_2") {
                    var county = place.address_components[i].long_name;
                }
                if (place.address_components[i].types[j] == "country") {
                    var country = place.address_components[i].long_name;
                }

                if (place.address_components[i].types[j] == "postal_code") {
                    var post_code = place.address_components[i].long_name
                }
            }
        }
        document.getElementsByName('localization')[0].value = num + " " + address;

    }
}
var count_of_addresses = document.getElementById('count_of_addresses');
var address_elements = [];


count_of_addresses.addEventListener('change', () => {
    if (count_of_addresses.value >0) {

        if (address_elements.length != 0) {
            DeleteAddressElements();
        }
        for (var i = 0; i < count_of_addresses.value; i++) {
            var ele=CreateAddressElement(count_of_addresses.value-i);
            address_elements.push(ele);
            count_of_addresses.insertAdjacentElement('afterend', ele);
            
        }
    }
    else {
        alert('you can\'t input negative or zero value');
    }
});

function DeleteAddressElements() {
    for (var i = 0; i < address_elements.length; i++) {
        address_elements[i].remove();
    }
    address_elements=[];
}

function CreateAddressElement(index) {
    var div = document.createElement('div');
    div.classList.add('d-flex');
    div.classList.add('flex-column');

    var row0 = document.createElement('div');
    row0.classList.add('d-flex');

    var label = document.createElement('label');
    label.innerText = `address ${ index }`;

    row0.appendChild(label);


    var row1 = document.createElement('div');
    row1.classList.add('d-grid');
    row1.classList.add('goods_elements')


    var inpPreviousAddress = document.createElement('input');
    inpPreviousAddress.classList.add('control');
    inpPreviousAddress.classList.add('my-2');
    inpPreviousAddress.placeholder = 'Previous address | set "startpoint" if there is not';
    inpPreviousAddress.name = "AddressPre_" + index;
    inpPreviousAddress.required=true;

    var inpCurrentAddress = document.createElement('input');
    inpCurrentAddress.classList.add('control');
    inpCurrentAddress.classList.add('my-2');
    inpCurrentAddress.placeholder = 'Current address';
    inpCurrentAddress.name = "AddressCurr_" + index;
    inpCurrentAddress.required=true;

    

    

    row1.appendChild(inpCurrentAddress);
    row1.appendChild(inpPreviousAddress);

    var row2 = document.createElement('div');
    row2.classList.add('d-grid');
    row2.classList.add('goods_elements')

    var inpTime = document.createElement('input');
    inpTime.classList.add('control');
    inpTime.classList.add('my-2');
    inpTime.placeholder = 'Time';
    inpTime.name = "AddressTime_" + index;
    inpTime.required=true;

    row2.appendChild(inpTime);

    div.appendChild(row0);
    div.appendChild(row1);
    div.appendChild(row2);

    return div

}
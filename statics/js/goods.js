var count_of_goods = document.getElementById('count_of_goods');
var goods_elements = [];


count_of_goods.addEventListener('change', () => {
    if (count_of_goods.value >0) {

        if (goods_elements.length != 0) {
            DeleteGoodsElements();
        }
        for (var i = 0; i < count_of_goods.value; i++) {
            var ele=CreateGoodsElement(count_of_goods.value-i);
            goods_elements.push(ele);
            count_of_goods.insertAdjacentElement('afterend', ele);
            
        }
    }
    else {
        alert('you can\'t input negative or zero value');
    }
});

function DeleteGoodsElements() {
    for (var i = 0; i < goods_elements.length; i++) {
        goods_elements[i].remove();
    }
    goods_elements=[];
}

function CreateGoodsElement(index) {
    var div = document.createElement('div');
    div.classList.add('d-flex');
    div.classList.add('flex-column');
    

    var row0 = document.createElement('div');
    row0.classList.add('d-flex');

    var label = document.createElement('label');
    label.innerText = `goods ${ index }`;

    row0.appendChild(label);

    var row1 = document.createElement('div');
    row1.classList.add('d-grid');
    row1.classList.add('goods_elements')


    var inpAddress = document.createElement('input');
    inpAddress.classList.add('control');
    inpAddress.classList.add('my-2');
    inpAddress.name = "GoodAddress_" + index;
    inpAddress.placeholder = 'Address';
    inpAddress.required=true;

    row1.appendChild(inpAddress);

    var row2 = document.createElement('div');
    row2.classList.add('d-grid');
    row2.classList.add('goods_elements')


    var inpWeight = document.createElement('input');
    inpWeight.classList.add('control');
    inpWeight.classList.add('my-2');
    inpWeight.setAttribute("name","GoodWeight_" + index);
    inpWeight.placeholder = 'Weight';
    inpWeight.required=true;

    row2.appendChild(inpWeight);

    div.appendChild(row0);
    div.appendChild(row1);
    div.appendChild(row2);
    console.log(div);
    return div;

}
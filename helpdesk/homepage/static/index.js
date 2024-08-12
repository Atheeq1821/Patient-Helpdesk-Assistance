document.addEventListener('DOMContentLoaded', function() {
    const policy = document.getElementById('policy_dd');
    const insurer = document.getElementById('insurer_dd');

    const options = {
        hdfc: [
            {text: 'myHealth Suraksha', value: 'suraksha'},
            {text: 'myHealth Medisure', value: 'medisure'},
            {text: 'Optima Secure', value: 'optimasecure'},
            {text: 'Energy', value: 'energy'}
        ],
        care: [
            {text: 'Care', value: 'care'},
            {text: 'Care Supreme', value: 'caresupreme'},
            {text: 'Care Senior', value: 'caresenior'},
            {text: 'Care Plus Youth', value: 'careplusyouth'},
            {text: 'Care Heart', value: 'careheart'},
            {text: 'Care Classic', value: 'careclassic'}
        ],
        nivabupa:[
            {text: 'Go Active', value:'goactive'},
            {text: 'HeartBeat Gold', value:'heartbeat'},
            {text: 'Health Pulse' , value:'healthpulse'},
            {text: 'Senior First', value:'seniorfirstgold'},
        ],
        bajajallianz:[
            {text:"Health Guard", value:'healthguardsilver'},
            {text:"Health Ensure Family", value:'healthensurefamily'},
            {text:"Health Care Supreme", value:'healthcaresupreme'},
            {text:"Silver Health", value:'healthguardplatinum'}
        ]
    };

    insurer.addEventListener('change', function() {
        const selectedValue = this.value;
        const optionsList = options[selectedValue] || [];
        console.log('Options list:', optionsList); 
        // Clear previous options
        policy.innerHTML = '<option value="" disabled selected>Choose your Policy</option>';

        // Populate new options
        optionsList.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.text;
            policy.appendChild(optionElement);
        });
    });
});

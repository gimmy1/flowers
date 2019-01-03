import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Form from '../Form'

const testData = [
    {
        formType: 'Register',
        formData: {
            username: '',
            email: '',
            password: ''
        },
        // isAuthenticated: false,
        // loginUser: jest.fn()
    },
    {
        formType: 'Login',
        formData: {
            email: '',
            password: ''
        },
        // isAuthenticated: false,
        // loginUser: jest.fn()
    }
]

testData.forEach((el) => {
    test(`${el.formType} Form renders properly`, () => {
        const component = <Form formType={el.formType} formData={el.formData}/>;
        const wrapper = shallow(component);
        const h1 = wrapper.find('h1')
        expect(h1.length).toBe(1)
        const formGroup = wrapper.find('.field')
        expect(formGroup.length).toBe(Object.keys(el.formData).length)
    });
    // test(`${el.formType} Form renders a snapshot properly`, () => {
    //     const component = <Form formtype={el.formType} formData={el.formData}/>
    //     const tree = renderer.create(component).toJSON();
    //     console.log(tree)
    //     expect(tree).toMatchSnapshot()
    // });
});
const config = {
    content: ['./src/**/*.{html,js,svelte,ts}'],

    darkMode: 'class',

    theme: {
        extend: {
            colors: {
                //     purple: '#631a86',
                //     pink: '#c45ab3',
                //     red: '#f45866',
                //     white: '#efe9f4',
                //     blue: '#08b2e3'
            }
        },
        fontFamily: {
            sans: ['Graphik', 'sans-serif'],
            serif: ['Merriweather', 'serif']
        }
    },

    plugins: [
        require('flowbite/plugin'),
        require('@tailwindcss/forms'),
        function({ addBase, theme }) {
            function extractColorVars(colorObj, colorGroup = '') {
                return Object.keys(colorObj).reduce((vars, colorKey) => {
                    const value = colorObj[colorKey];

                    const newVars =
                        typeof value === 'string' ? {
                            [`--color${colorGroup}-${colorKey}`]: value
                        } :
                        extractColorVars(value, `-${colorKey}`);

                    return {...vars, ...newVars };
                }, {});
            }

            addBase({
                ':root': extractColorVars(theme('colors')),
            });
        },
    ]
};

module.exports = config;
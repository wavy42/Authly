# Authly Frontend Example

This project serves as an example frontend implementation for Authly, a simple authentication system. Authly is designed to showcase backend integration with bubble IDs/keys for secure communication. This example uses Svelte, integrates Tailwind CSS, and is entirely client-sided.

## Getting Started

### Prerequisites

Make sure you have Node.js installed on your machine.

### Installation

Install dependencies:

```bash
npm install
```

### Configuration

Before running the application, configure the backend bubble ID/key in the src/config.js file.

```js
// src/config.js
const config = {
	// Other configurations...
	backend: {
		bubbleId: 'your-backend-bubble-id'
	}
};

export default config;
```

Replace 'your-backend-bubble-id' with the actual bubble ID and key from your Authly backend.

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

Visit <http://localhost:5173> in your browser to see the Authly Frontend in action.

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.

## Features

- User registration
- Tailwind CSS for styling
- Client-side integration with Authly backend
- Easy-to-understand example for backend implementation

## components

<https://github.com/keenethics/svelte-notifications>,
<https://tailwindcomponents.com/>,
<https://github.com/estevanmaito/windmill-dashboard>,
<https://tailwindui.com/>

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests. Your feedback and suggestions are valuable!

## License

Authly is licensed under the MIT License with additional clauses:

- **Copyleft Clause**</br>
  Any modifications, adaptations, or derivative works based on this software must be made publicly available on GitHub with proper attribution to the original developer wavy42 by adding a link to the original repository.

- **Commercial Use Attribution Clause**</br>
  For any commercial use of this software, proper attribution to the original developer wavy42 is required, and a link to the original repository on GitHub must be provided.

module.exports = {
  css: {
    loaderOptions: {
      sass: {
        additionalData: `
          @import '@/styles/variables.scss';
        `
      },
      // less: {
      //   lessOptions: {
      //     modifyVars: {
      //       'primary-color': 'rgb(127, 99, 244)'
      //     },
      //     javascriptEnabled: true,
      //   },
      // },
    }
  }
}
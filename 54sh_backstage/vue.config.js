module.exports = {
  css: {
    loaderOptions: {
      sass: {
        additionalData: `
          @import '@/styles/variables.scss';
          @import '@/styles/base.scss';
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
